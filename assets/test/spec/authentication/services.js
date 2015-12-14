describe('Service: Authentication. checking APIs and definitions', function(){

    // executed before each "it" is run.
    beforeEach(function(){
        module('ndtApp');
        module('ndtApp.authentication.services');
    });

    var Authentication, $cookieStore;
    var httpBackend = null;
    // inject your service for testing.
    // The _underscores_ are a convenience thing
    // so you can have your variable name be the
    // same as your injected service.
    beforeEach(inject(function ($httpBackend, _Authentication_, _$cookieStore_) {
        httpBackend = $httpBackend;
        Authentication = _Authentication_;
        $cookieStore = _$cookieStore_;
    }));

    // make sure no expectations were missed in your tests.
    // (e.g. expectGET or expectPOST)
    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
        $cookieStore.remove ('authenticatedAccount');
    });


    it("should have Authentication service be define", function(){
        expect(Authentication).toBeDefined();
    });

    it('should not have a user existing upon starting up', function() {
        expect(Authentication.getAuthenticatedAccount()).toBe(null);
    });

    it('should not have any user authenticated in the beginning', function() {
        expect(Authentication.isAuthenticated()).toBe(false);
    });


    it('should send a post request to logout API', function() {
        httpBackend.expectPOST(/\/accounts\/logout/, undefined).respond('');
        Authentication.logout();
        httpBackend.flush();
    });

    it('should send a post request to deactivate API', function() {
        httpBackend.expectPOST(/\/accounts\/deactivate/, undefined).respond('');
        Authentication.deactivate();
        httpBackend.flush();
    });

    it('should send a post request to register API', function() {
        // register actually can call both register and login
        httpBackend.expectPOST(/\/accounts\/register/, undefined).respond('');
        httpBackend.expectPOST(/\/accounts\/login/, undefined).respond('');
        Authentication.register();
        httpBackend.flush();
    });

    it('should send a post request to updatePassword API', function() {
        // register actually can call both register and login
        httpBackend.expectPOST(/\/accounts\/updatepassword/, undefined).respond('');
        Authentication.updatePassword();
        httpBackend.flush();
    });

});


describe('Service: Authentication, Checking login functionalities', function(){

    // executed before each "it" is run.
    beforeEach(function(){
        module('ndtApp');
        module('ndtApp.authentication.services');
    });

    var Authentication;
    var httpBackend = null;
    // inject your service for testing.
    // The _underscores_ are a convenience thing
    // so you can have your variable name be the
    // same as your injected service.
    beforeEach(inject(function ($httpBackend, _Authentication_) {
        httpBackend = $httpBackend;
        Authentication = _Authentication_;
    }));

    // make sure no expectations were missed in your tests.
    // (e.g. expectGET or expectPOST)
    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });

    // mock successful server response to login request
    var loginResponse = {
        "status":"Success",
        "account":{
            "email":"test@ispfy.com",
            "username":"test",
            "created_at":"2015-09-25T21:45:51.053266Z",
            "updated_at":"2015-10-28T13:59:30.193767Z"
        },
        "message":"You are logged in successfully."
    };

    var returnedData;
    var errorStatus = '';
    var handler;
    // Listen to callbacks of loging function and mimicking callbacks
    beforeEach(function() {
        returnedData = [];
        errorStatus = '';
        handler = {
            success: function(data) {
                returnedData = data;
            },
            error: function(data) {
                errorStatus = data.status;
            }
        };
        spyOn(handler, 'success').and.callThrough();
        spyOn(handler, 'error').and.callThrough();
    });

    it('should return an array of logged user on success', function() {
        var response = loginResponse;

        httpBackend.expectPOST(/\/accounts\/login/).respond(response);
        Authentication.login().then(handler.success, handler.error);
        httpBackend.flush();

        expect(handler.success).toHaveBeenCalled();
        expect(returnedData).toEqual(response);
        expect(handler.error).not.toHaveBeenCalled();
        expect(errorStatus).toEqual('');
    });

    it('Login return the status on error', function() {
        httpBackend.expectPOST(/\/accounts\/login/).respond(404, {"status": 404});
        Authentication.login().then(handler.success, handler.error);
        httpBackend.flush();

        expect(handler.error).toHaveBeenCalled();
        expect(errorStatus).toEqual(404);
        expect(handler.success).not.toHaveBeenCalled();
        expect(returnedData).toEqual([]);
    });

});