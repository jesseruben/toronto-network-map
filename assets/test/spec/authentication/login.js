describe('Controller: LoginController', function() {
    beforeEach(module('ndtApp'));

    // Mocking Authentication service included in a separate file
    beforeEach(module('AuthenticationMock'));
    var Authentication;
    // Mock services and spy on methods, $q is for async call
    beforeEach(inject(function($q, _Authentication_) {
        deferred = $q.defer();
        Authentication = _Authentication_;
        spyOn(Authentication, 'login').and.callThrough();
        spyOn(Authentication, 'logout').and.returnValue(deferred.promise);
    }));

    var LoginController;
    var error1= {email:true};
    var error2= {required:true};
    var email = 'test@gmail.com';
    var password = 'Asl239djnc5';

    beforeEach(inject(function($controller) {
        scope = {};
        LoginController = $controller('LoginController', {
            Authentication : Authentication
        });
    }));

    it('should have model defined and LoginController.model.name is equal to controllerAs vm test', function() {
        expect(LoginController).toBeDefined();
        expect(LoginController.model).toBeDefined();
        expect(LoginController.model.name).toEqual("controllerAs vm test");
    });

    it('should not have a property called vm', function() {
        expect(LoginController.vm).toBeUndefined();
    });

    it('Should return proper text when getError function is called from the form', function(){
        expect(LoginController.getError).toBeDefined();
        expect(LoginController.getError(error1)).toEqual('Please enter a valid email address.');
        expect(LoginController.getError(error2)).toEqual('This field is required');
    });

    it('should call Authentication login', function () {
        LoginController.login();
        expect(Authentication.login).toHaveBeenCalled();
        expect(Authentication.login.calls.count()).toBe(1);
    });
});