const url = "http://127.0.0.1:6399/customers";
const full_customer_url = "http://127.0.0.1:6399/full_customer/";
const individual_customer_url = "http://127.0.0.1:6399/customers/";

const vm = new Vue({
	el: '#app',   
	data: { 
			editmode: 0,
			imsieditmode: 0,
			imeieditmode: 0,
			ID: -1,
			results: [],
			customer_results: [],
			sim_results: [],
			firstname: '-',
			lastname: '-',
			age: '-',
			gender: '-',
			nationality: '-',
			street: '-',
			zip: '-',
			city: '-',
			email: '-',
			msisdn: '-',
			IMSI: '-',
			IMSIPtr: null,
			IMEI: '-',
			IMEIPtr: null,
			device: '-',
			device_type: '-',
			image: ''
	},
	methods: {
		updateDetails: function(customerID) {			


				axios.get(full_customer_url + customerID).then(response => {
					this.ID = customerID
	        		this.customer_results = response.data
	        		this.firstname = this.customer_results['Firstname']
	        		this.lastname = this.customer_results['Lastname']
	        		this.age = this.customer_results['Age']
	        		this.gender = this.customer_results['Sex']
	        		this.nationality = this.customer_results['Nationality']
	        		this.street = this.customer_results['Street']
	        		this.zip = this.customer_results['Zip']
	        		this.city = this.customer_results['City']
	        		this.email = this.customer_results['Email']
	        		
	        		this.msisdn = this.customer_results['sim']['MSISDN']
	        		this.IMSI = this.customer_results['sim']['IMSI']        		
	        		this.IMSIPtr = this.customer_results['sim']['ID']

	        		this.device_type = this.customer_results['equipment']['product']['Type']
	        		this.device = this.customer_results['equipment']['product']['Model']
	        		this.IMEI = this.customer_results['equipment']['IMEI']
	        		this.IMEIPtr = this.customer_results['equipment']['ID']

	        		this.image = 'http://127.0.0.1:6399' + this.customer_results['equipment']['product']['ImageURL']
	        		
	        	})
		},
		editNewCustomer: function() {
			this.firstname = ''
    		this.lastname = ''
    		this.age = ''
    		this.gender = ''
    		this.nationality = ''
    		this.street = ''
    		this.zip = ''
    		this.city = ''
    		this.email = ''
    		this.msisdn = ''
    		this.IMSI = ''
    		this.IMSIPtr = ''
    		this.device_type = ''
    		this.device = ''
    		this.IMEI = ''
    		this.IMEIPtr = ''
    		this.image = ''

    		this.newcustomermode = 1
    		this.enableEditMode()
		},
		editCustomer: function(customerID) {
			if (this.newcustomermode == 1) {
				axios.post(url, {					
					Firstname: this.firstname,
					Lastname: this.lastname,
					Age: this.age,
					Sex: this.gender,
					Street: this.street,
					Zip: this.zip,
					City: this.city,
					Email: this.email,
					IMSIPtr: this.IMSIPtr,
					IMEIPtr: this.IMEIPtr,
					Nationality: this.nationality
				}).then(response => {
					this.editmode = 0
				})
			}
			else {
				axios.put(individual_customer_url + customerID, {
					ID: this.ID,
					Firstname: this.firstname,
					Lastname: this.lastname,
					Age: this.age,
					Sex: this.gender,
					Street: this.street,
					Zip: this.zip,
					City: this.city,
					Email: this.email,
					IMSIPtr: this.IMSIPtr,
					IMEIPtr: this.IMEIPtr,
				}).then(response => {
					this.editmode = 0
				})
			}
			location.reload();											
		},
		DeleteCustomer: function() {
			var r = confirm("Are you sure you want to delete this customer?")
			if (r == true) {
				axios.delete(individual_customer_url + this.ID).then(response => {
					location.reload();											
				})
			}
		},
		AddSimAndEquipment: function() {
			this.imsieditmode = 1;
			this.imeieditmode = 1;
		},
		enableEditMode: function() {
			this.editmode = 1
		},
		cancelEditCustomer: function() {
			this.editmode = 0			
		},
		enableIMSIEditMode: function() {
			this.imsieditmode = 1
		},
		cancelIMSIEditCustomer: function() {
			this.imsieditmode = 0			
		}		
	},
	computed: {
		noSimAndEquipment: function() {
			if (this.ID == -1) {
				return false
			}
			if (this.IMSIPtr == '' && this.IMEIPtr == '') {
				return true;				
			}
			else {
				return false;
			}
		},
		SimOrEquipment: function() {
			if (this.ID == -1) {
				return false
			}
			if (this.IMSIPtr != '' || this.IMEIPtr != '') {
				return true;				
			}
			else {
				return false;
			}
		}
	},
    mounted() {
      axios.get(url).then(response => {
        this.results = response.data
      })
    }
  });