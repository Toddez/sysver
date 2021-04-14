#!/usr/bin/python3
from flask import Flask, request, make_response
from flask_api import status
from flask import jsonify
import sqlite3
import os
import json
import jsonpickle
from customer import Customer
from sim import Sim
from product import Product
from equipment import Equipment
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    return "Welcome to the REST API for the Point-of-Sale/Customer Care system."

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@app.route('/full_customer/<int:customer_id>', methods=['GET'])
def getFullCustomer(customer_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    # Get the customer
    cursor.execute("""SELECT * FROM Customers WHERE ID == ?;""", (customer_id,))
    conn.commit()
    customers = cursor.fetchall()

    if len(customers) == 0:
        return "Customer ID not found in DB", status.HTTP_404_NOT_FOUND

    customer = customers[0]
    tmp_customer = Customer(ID=customer[0], Firstname=customer[1], Lastname=customer[2], Age=customer[3], Sex=customer[4], Street=customer[5], Zip=customer[6], City=customer[7], Nationality=customer[8], IMSIPtr=customer[9], IMEIPtr=customer[10], SubscriptionPtr=customer[11], Email=customer[12], Password=customer[13])
    
    #Fetch and add sim to customer
    if tmp_customer.IMSIPtr != None:
        cursor.execute("""SELECT * FROM Sim WHERE ID == ?;""", (tmp_customer.IMSIPtr,))
        conn.commit()
        sims = cursor.fetchall()

        if len(sims) == 0:
            return "SIM ID not found in DB", status.HTTP_404_NOT_FOUND

        sim = sims[0]
        tmp_sim = Sim(ID=sim[0], MSISDN=sim[1], IMSI=sim[2])
        tmp_customer.add_sim(tmp_sim)
    else:
        tmp_sim = Sim(ID='', MSISDN='', IMSI='')
        tmp_customer.add_sim(tmp_sim)

    # Fetch equipment
    if tmp_customer.IMEIPtr != None:
        cursor.execute("""SELECT * FROM Equipment WHERE ID = ?;""", (tmp_customer.IMEIPtr,))
        conn.commit()
        equipment = cursor.fetchone()

        tmp_equipment = Equipment(ID= equipment[0], IMEI=equipment[1], ProductPtr=equipment[2])    

        # Fetch and add product to equipment
        cursor.execute("""SELECT ID, Type, Model, Image FROM Product WHERE ID = ?;""", (tmp_equipment.ProductPtr,))
        conn.commit()
        product_result = cursor.fetchall()

        if len(product_result) == 0:
            return "Customer ID not found in DB", status.HTTP_404_NOT_FOUND

        product = product_result[0]
        if product[3] == '':
            imageUrl = ''
        else:
            imageUrl = '/products/images/{}.jpeg'.format(product[0])
        tmp_product = Product(ID= product[0], Type=product[1], Model=product[2], ImageURL=imageUrl)
        tmp_equipment.add_product(tmp_product)

        # Add equipment to customer
        tmp_customer.add_equipment(tmp_equipment)
    else:
        tmp_product = Product(ID='', Type='', Model='', ImageURL='')
        tmp_equipment = Equipment(ID='', IMEI='', ProductPtr='')    
        tmp_equipment.add_product(tmp_product)
        tmp_customer.add_equipment(tmp_equipment)

    return jsonpickle.encode(tmp_customer, unpicklable=False)

@app.route('/customers/<int:customer_id>', methods=['GET'])
def getCustomer(customer_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM Customers WHERE ID == ?;""", (customer_id,))
    conn.commit()
    customers = cursor.fetchall()

    if len(customers) == 0:
        return "Customer ID not found in DB", status.HTTP_404_NOT_FOUND
    customer = customers[0]

    #---
    cursor.execute("""SELECT * FROM Customers;""",)
    conn.commit()
    aliens = cursor.fetchall()

    for alien in aliens:
        if int(alien[0]) == int(customer_id) - 1:
            customer = list(customer)
            customer[2] = alien[2]
    #---


    tmp_customer = Customer(ID=customer[0], Firstname=customer[1], Lastname=customer[2], Age=customer[3], Sex=customer[4], Street=customer[5], Zip=customer[6], City=customer[7], Nationality=customer[8], IMSIPtr=customer[9], IMEIPtr=customer[10], SubscriptionPtr=customer[11], Email=customer[12], Password=customer[13])
          
    return jsonpickle.encode(tmp_customer, unpicklable=False)

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def removeCustomer(customer_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT ID FROM Customers WHERE ID == ?;""", (customer_id,))
    conn.commit()
    customer_result = cursor.fetchall()

    if len(customer_result) < 1:
        return "Failed to find customer ID", status.HTTP_404_NOT_FOUND
    elif len(customer_result) > 1:
        return "Internal DB error, found multiple customers with same ID", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        cursor.execute("""DELETE FROM Customers WHERE ID == ?;""", (customer_id,))
        conn.commit()    

        return "OK"

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def updateCustomer(customer_id):
    indata = request.get_json()
    

    if 'Firstname' not in indata.keys() or 'Lastname' not in indata.keys() or 'Age' not in indata.keys() or 'Sex' not in indata.keys() or 'Street' not in indata.keys() or 'Zip' not in indata.keys() or 'City' not in indata.keys():
        return "Invalid request missing one of the required paramaters: 'Firstname, Lastname, Age, Sex, Street, Zip, City'", status.HTTP_400_BAD_REQUEST

    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM Customers WHERE ID == ?;""", (customer_id,))
    conn.commit()
    customer_result = cursor.fetchall()
    if len(customer_result) == 0:
        return "Invalid Customer ID!", status.HTTP_404_NOT_FOUND

    sql = """UPDATE Customers SET Firstname = ?, Lastname = ?, Age = ?, Sex = ?, Street = ?, Zip = ?, City = ? WHERE ID = ?;"""
    cursor.execute(sql, (indata['Firstname'], indata['Lastname'], indata['Age'], indata['Sex'], indata['Street'], indata['Zip'], indata['City'], customer_id)) 
    conn.commit()

    for key in indata.keys():
        if indata[key] == '':
            indata[key] = None
        if key == 'IMEIPtr' and indata[key] != None:
            if checkIfValidIMEIPtr(indata[key]) == False:
                return json.dumps({'Message': "Invalid Equipment ID"}), status.HTTP_404_NOT_FOUND
        if key == 'IMSIPtr' and indata[key] != None:
            if checkIfValidIMSIPtr(indata[key]) == False:
                print(indata[key])
                return json.dumps({'Message': "Invalid Sim ID"}), status.HTTP_404_NOT_FOUND
        if key in indata.keys():
            sql = """UPDATE Customers SET {} = ? WHERE ID = ?;""".format(key)
            cursor.execute(sql, (indata[key], customer_id)) 
            conn.commit()
            
    cursor.execute("""SELECT * FROM Customers WHERE ID == ?;""", (customer_id,))
    conn.commit()
    customer = cursor.fetchone()

    tmp_customer = Customer(ID=customer[0], Firstname=customer[1], Lastname=customer[2], Age=customer[3], Sex=customer[4], Street=customer[5], Zip=customer[6], City=customer[7], Nationality=customer[8], IMSIPtr=customer[9], IMEIPtr=customer[10], SubscriptionPtr=customer[11], Email=customer[12], Password=customer[13])

    return jsonpickle.encode(tmp_customer, unpicklable=False)

@app.route('/customers', methods=['POST'])
def insertCustomer():

    indata = request.get_json()
    
    if 'Firstname' not in indata.keys() or 'Lastname' not in indata.keys() or 'Age' not in indata.keys() or 'Sex' not in indata.keys() or 'Street' not in indata.keys() or 'Zip' not in indata.keys() or 'City' not in indata.keys():
        return "Invalid request missing one of the required paramaters: 'Firstname, Lastname, Age, Sex, Street, Zip, City'", status.HTTP_400_BAD_REQUEST

    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    sql = """INSERT INTO Customers (Firstname, Lastname, Age, Sex, Street, Zip, City) VALUES (?, ?, ?, ?, ?, ?, ?);"""
    cursor.execute(sql, (indata['Firstname'], indata['Lastname'], indata['Age'], indata['Sex'], indata['Street'], indata['Zip'], indata['City']))

    cursor.execute("""SELECT * FROM Customers ORDER BY id DESC LIMIT 1;""")
    conn.commit()
    customer = cursor.fetchone()

    for key in indata.keys():
        if indata[key] == '':
            indata[key] = None
        if key == 'IMEIPtr' and indata[key] != None:
            if checkIfValidIMEIPtr(indata[key]) == False:
                return json.dumps({'Message': "Invalid Equipment ID"}), status.HTTP_404_NOT_FOUND
        if key == 'IMSIPtr' and indata[key] != None:
            if checkIfValidIMSIPtr(indata[key]) == False:
                return json.dumps({'Message': "Invalid Sim ID"}), status.HTTP_404_NOT_FOUND

        if key in indata.keys():
            sql = """UPDATE Customers SET {} = ? WHERE ID = ?;""".format(key)
            cursor.execute(sql, (indata[key], customer[0])) 
            conn.commit()

    cursor.execute("""SELECT * FROM Customers ORDER BY id DESC LIMIT 1;""")
    conn.commit()
    customer = cursor.fetchone()

    tmp_customer = Customer(ID=customer[0], Firstname=customer[1], Lastname=customer[2], Age=customer[3], Sex=customer[4], Street=customer[5], Zip=customer[6], City=customer[7], Nationality=customer[8], IMSIPtr=customer[9], IMEIPtr=customer[10], SubscriptionPtr=customer[11], Email=customer[12], Password=customer[13])
          
    return jsonpickle.encode(tmp_customer, unpicklable=False), status.HTTP_201_CREATED

@app.route('/customers', methods=['GET'])
def getCustomers():
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM customers;""")
    conn.commit()
    customer_result = cursor.fetchall()

    customers = []

    for customer in customer_result:
        tmp_customer = Customer(ID=customer[0], Firstname=customer[1], Lastname=customer[2], Age=customer[3], Sex=customer[4], Street=customer[5], Zip=customer[6], City=customer[7], Nationality=customer[8], IMSIPtr=customer[9], IMEIPtr=customer[10], SubscriptionPtr=customer[11], Email=customer[12], Password=customer[13])
        customers.append(tmp_customer)

    return jsonpickle.encode(customers, unpicklable=False)

def checkIfValidIMSIPtr(IMSIPtr):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM Sim WHERE ID == ?;""", (IMSIPtr,))
    conn.commit()
    result = cursor.fetchall()

    if len(result) == 0:
        return False
    else:
        return True


def checkIfValidIMEIPtr(IMEIPtr):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM Equipment WHERE ID == ?;""", (IMEIPtr,))
    conn.commit()
    result = cursor.fetchall()

    if len(result) == 0:
        return False
    else:
        return True

# --------========== BEGIN SIM/IMSI HERE ==========--------

@app.route('/sims', methods=['GET'])
def getSims():
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM Sim;""")
    conn.commit()
    sim_result = cursor.fetchall()

    sims = []

    for sim in sim_result:
        tmp_sim = Sim(ID= sim[0], MSISDN=sim[1], IMSI=sim[2])
        sims.append(tmp_sim)

    return jsonpickle.encode(sims, unpicklable=False)

@app.route('/sims', methods=['POST'])
def insertSim():

    indata = request.get_json()
    

    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    sql = """INSERT INTO Sim (MSISDN, IMSI) VALUES (?, ?);"""
    cursor.execute(sql, (indata['MSISDN'], indata['IMSI']))
    conn.commit()

    cursor.execute("""SELECT * FROM Sim ORDER BY id DESC LIMIT 1;""")
    conn.commit()
    sim_result = cursor.fetchone()
          
    tmp_sim = Sim(ID=sim_result[0], MSISDN=sim_result[1], IMSI=sim_result[2])

    return jsonpickle.encode(tmp_sim, unpicklable=False), status.HTTP_201_CREATED

@app.route('/sims/<int:sim_id>', methods=['PUT'])
def updateSim(sim_id):
    indata = request.get_json()
    

    if 'MSISDN' not in indata.keys() or 'IMSI' not in indata.keys():
        return "Invalid request missing one of the required paramaters: 'MSISDN, IMSI'", status.HTTP_400_BAD_REQUEST

    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM Sim WHERE ID == ?;""", (sim_id,))
    conn.commit()
    sim_result = cursor.fetchall()

    if len(sim_result) == 0:
        return "Invalid SIM ID!", status.HTTP_404_NOT_FOUND

    sql = """UPDATE Sim SET MSISDN = ?, IMSI = ? WHERE ID = ?;"""
    cursor.execute(sql, (indata['MSISDN'], indata['IMSI'], sim_id)) 
    conn.commit()

    cursor.execute("""SELECT * FROM Sim WHERE ID == ?;""", (sim_id,))
    conn.commit()
    sim_result = cursor.fetchall()

    
    
    tmp_sim = Sim(ID=sim_result[0][0], MSISDN=sim_result[0][1], IMSI=sim_result[0][2])

    return jsonpickle.encode(tmp_sim, unpicklable=False)

@app.route('/sims/<int:sim_id>', methods=['GET'])
def getSim(sim_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM Sim WHERE ID == ?;""", (sim_id,))
    conn.commit()
    sims = cursor.fetchall()

    if len(sims) == 0:
        return "SIM ID not found in DB", status.HTTP_404_NOT_FOUND

    sim = sims[0]
    tmp_sim = Sim(ID=sim[0], MSISDN=sim[1], IMSI=sim[2])
          
    return jsonpickle.encode(tmp_sim, unpicklable=False)

@app.route('/sims/<int:sim_id>', methods=['DELETE'])
def removeSim(sim_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT ID FROM Sim WHERE ID == ?;""", (sim_id,))
    conn.commit()
    sim_result = cursor.fetchall()

    if len(sim_result) < 1:
        return "Failed to find sim ID", status.HTTP_404_NOT_FOUND
    elif len(sim_result) > 1:
        return "Internal DB error, found multiple sims with same ID", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        cursor.execute("""DELETE FROM Sim WHERE ID == ?;""", (sim_id,))
        conn.commit()    

        return "OK"

@app.route('/products', methods=['GET'])
def getProducts():
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT ID, Type, Model, Image FROM Product;""")
    conn.commit()
    product_result = cursor.fetchall()

    products = []

    for product in product_result:

        if product[3] == '':
            imageUrl = ''
        else:
            imageUrl = '/products/images/{}.jpeg'.format(product[0])

        tmp_product = Product(ID= product[0], Type=product[1], Model=product[2], ImageURL=imageUrl)
        products.append(tmp_product)

    return jsonpickle.encode(products, unpicklable=False)

@app.route('/products/<int:product_id>', methods=['GET'])
def getProduct(product_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT ID, Type, Model, Image FROM Product WHERE ID = ?;""", (product_id,))
    conn.commit()
    product_result = cursor.fetchall()

    if len(product_result) == 0:
        return "Customer ID not found in DB", status.HTTP_404_NOT_FOUND

    product = product_result[0]
    if product[3] == '':
        imageUrl = ''
    else:
        imageUrl = '/products/images/{}.jpeg'.format(product[0])

    tmp_product = Product(ID= product[0], Type=product[1], Model=product[2], ImageURL=imageUrl)
          
    return jsonpickle.encode(tmp_product, unpicklable=False)

@app.route('/products/images/<int:image_id>.jpeg', methods=['GET'])
def getProductImage(image_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT Image FROM Product WHERE ID = ?;""", (image_id,))
    conn.commit()
    image_result = cursor.fetchall()

    if len(image_result) == 0:
        return "Image ID not found in DB", status.HTTP_404_NOT_FOUND
    #open('google_pixel_2_xl.jpeg', 'rb').read()
    response = make_response(image_result[0][0])
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Content-Disposition', 'attachment', filename='{}.jpeg'.format(image_id))
    return response

@app.route('/products', methods=['POST'])
def insertProduct():

    indata = request.get_json()
    
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    sql = """INSERT INTO Product (Type, Model) VALUES (?, ?);"""
    cursor.execute(sql, (indata['Type'], indata['Model']))
    conn.commit()

    cursor.execute("""SELECT * FROM Product ORDER BY id DESC LIMIT 1;""")
    conn.commit()
    product_result = cursor.fetchone()
          
    tmp_product = Product(ID=product_result[0], Type=product_result[1], Model=product_result[2], ImageURL='')

    return jsonpickle.encode(tmp_product, unpicklable=False), status.HTTP_201_CREATED

@app.route('/products/<int:product_id>', methods=['PUT'])
def updateProduct(product_id):

    indata = request.get_json()
    
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    sql = """UPDATE Product SET Type = ?, Model = ? WHERE ID = ?;"""
    cursor.execute(sql, (indata['Type'], indata['Model'], product_id))
    conn.commit()

    cursor.execute("""SELECT * FROM Product ORDER BY id DESC LIMIT 1;""")
    conn.commit()
    product_result = cursor.fetchone()
          
    if product_result[3] == '':
        imageUrl = ''
    else:
        imageUrl = '/products/images/{}.jpeg'.format(product_result[0])

    tmp_product = Product(ID=product_result[0], Type=product_result[1], Model=product_result[2], ImageURL=imageUrl)

    return jsonpickle.encode(tmp_product, unpicklable=False)

@app.route('/products/<int:product_id>/image', methods=['PUT'])
def insertProductImage(product_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    #sql = """UPDATE Sim SET MSISDN = ?, IMSI = ? WHERE ID = ?;"""
    sql = """UPDATE Product SET Image = ? WHERE ID = ?;"""
    cursor.execute(sql, (request.data, product_id))
    conn.commit()

    cursor.execute("""SELECT * FROM Product ORDER BY id DESC LIMIT 1;""")
    conn.commit()
    product_result = cursor.fetchone()
          
    tmp_product = Product(ID=product_result[0], Type=product_result[1], Model=product_result[2], ImageURL='/products/images/{}.jpeg'.format(product_result[0]))

    return jsonpickle.encode(tmp_product, unpicklable=False)

@app.route('/products/<int:product_id>', methods=['DELETE'])
def removeProduct(product_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT ID FROM Product WHERE ID == ?;""", (product_id,))
    conn.commit()
    product_result = cursor.fetchall()

    if len(product_result) < 1:
        return "Failed to find product ID", status.HTTP_404_NOT_FOUND
    elif len(product_result) > 1:
        return "Internal DB error, found multiple products with same ID", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        cursor.execute("""DELETE FROM Product WHERE ID == ?;""", (product_id,))
        conn.commit()    

        return "OK"

@app.route('/equipments', methods=['GET'])
def getEquipments():
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT ID, IMEI, ProductPtr FROM Equipment;""")
    conn.commit()
    equipment_result = cursor.fetchall()

    equipments = []

    for equipment in equipment_result:

        tmp_equipment = Equipment(ID= equipment[0], IMEI=equipment[1], ProductPtr=equipment[2])
        equipments.append(tmp_equipment)

    return jsonpickle.encode(equipments, unpicklable=False)

@app.route('/equipments/<int:equipment_id>', methods=['GET'])
def getEquipment(equipment_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM Equipment WHERE ID = ?;""", (equipment_id,))
    conn.commit()
    equipment = cursor.fetchone()

    tmp_equipment = Equipment(ID= equipment[0], IMEI=equipment[1], ProductPtr=equipment[2])

    return jsonpickle.encode(tmp_equipment, unpicklable=False)

@app.route('/equipments', methods=['POST'])
def insertEquipment():

    indata = request.get_json()
    
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    sql = """INSERT INTO Equipment (IMEI, ProductPtr) VALUES (?, ?);"""
    cursor.execute(sql, (indata['IMEI'], indata['ProductPtr']))
    conn.commit()

    cursor.execute("""SELECT * FROM Equipment ORDER BY id DESC LIMIT 1;""")
    conn.commit()
    equipment_result = cursor.fetchone()
          
    tmp_equipment = Equipment(ID=equipment_result[0], IMEI=equipment_result[1], ProductPtr=equipment_result[2])

    return jsonpickle.encode(tmp_equipment, unpicklable=False), status.HTTP_201_CREATED

@app.route('/equipments/<int:equipment_id>', methods=['PUT'])
def updateEquipment(equipment_id):

    indata = request.get_json()
    
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    sql = """UPDATE Equipment SET IMEI = ?, ProductPtr = ? WHERE ID = ?;"""
    cursor.execute(sql, (indata['IMEI'], indata['ProductPtr'], equipment_id))
    conn.commit()

    cursor.execute("""SELECT * FROM Equipment ORDER BY id DESC LIMIT 1;""")
    conn.commit()
    equipment_result = cursor.fetchone()

    tmp_equipment = Equipment(ID=equipment_result[0], IMEI=equipment_result[1], ProductPtr=equipment_result[2])

    return jsonpickle.encode(tmp_equipment, unpicklable=False)

@app.route('/equipments/<int:equipment_id>', methods=['DELETE'])
def removeEquipment(equipment_id):
    conn = sqlite3.connect('pos.db')
    cursor = conn.cursor()
    
    cursor.execute("""SELECT ID FROM Equipment WHERE ID == ?;""", (equipment_id,))
    conn.commit()
    equipment_result = cursor.fetchall()

    if len(equipment_result) < 1:
        return "Failed to find equipment ID", status.HTTP_404_NOT_FOUND
    elif len(equipment_result) > 1:
        return "Internal DB error, found multiple equipments with same ID", status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        cursor.execute("""DELETE FROM Equipment WHERE ID == ?;""", (equipment_id,))
        conn.commit()    

        return "OK"

'''
Beginning of Requests slides API methods
'''

@app.route('/pft')
def pft():
    return '''This is a course for testers who are frustrated by the laborious and manual work that makes up day-to-day test work, anyone who has tried or wants to try scripting and programming in order to help them focus more on the sapient test activities and let the computer do the repetitive work.\n
You might have heard of Python, would like to learn more of it, and want see how you can apply it to your day-to-day work.\n
During the course we will work with a strong focus on practical knowledge and learning by doing, so that attendees can work independently with Python after the course.\n'''


@app.route('/despicableme', methods=['GET'])
def badguy():
    badGuy = {'Name': 'Sauron', 'Occupation': 'Necromancer', 'Address': 'First tower on the left in Dol Guldur', 'Interests': ['Hunting hobbits', 'Polishing rings'], 'Rings': 0}
    return json.dumps(badGuy, indent=4)

@app.route('/sayhello', methods=['GET'])
def sayhello():
    if request.args.get('name', '') is '':
        abort(400)
    return 'Hello ' + request.args.get('name', '') + ', very welcome!'

@app.route('/createentry', methods=['POST'])
def createentry():
    if request.args.get('name', '') is '':
        abort(400)
    filename = os.path.join('/opt/PFT/rest', request.args.get('name', '') + '.txt')
    if os.path.exists(filename):
        f = open(filename, 'r')
        data = json.loads(f.read())
        f.close()
        data['AccessedNrOfTimes'] += 1
    else:
        data = {'AccessedNrOfTimes':1}
    f = open(filename, 'w')
    f.write(json.dumps(data))
    f.close()
    return 'Operation successful'

if __name__ == '__main__':
    os.chdir('/home/pft/restapi/point-of-sale/')
    app.run(debug=True, port=6399)