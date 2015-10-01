/**
 * INSPINIA - Responsive Admin Theme
 *
 */

/**
 * MainCtrl - controller
 */
function MainCtrl() {

    this.userName = 'Example user';
    this.helloText = 'Welcome in SeedProject';
    this.descriptionText = 'It is an application skeleton for a typical AngularJS web app. You can use it to quickly bootstrap your angular webapp projects and dev environment for these projects.';

	/**
	 * persons - Data used in Tables view for Data Tables plugin
	 */
	this.persons = [
	    {
	        document__number: '26610217874',
	        name: 'Sandro Alexandre Salles',
	        physicaladdress__street_full: 'Rua Dom Pero Leitão, 140',
	        physicaladdress__street__neighborhood__name: 'Vila Gumercindo',
	        physicaladdress__street__neighborhood__city__name: 'São Paulo',
	        physicaladdress__street__neighborhood__city__state__name: 'São Paulo/SP',
	        telephone__number_full: '(11) 4562-7557',
	        cellphone__number_full: '(11) 99203-9014',
	        nature: 'F',
	    }
	];


};





// Other 
angular
    .module('inspinia')
    .controller('MainCtrl', MainCtrl)