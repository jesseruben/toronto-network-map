(function () {
  'use strict';
    /**
     * This config is responsible of using html5 routing and replace the # in the browsers
     * in older browsers angular will fall back to # routing
     *  Remember to add it to ndtApp.js as dependencies
     */
  angular
    .module('ndtApp')
    .config(config);

  config.$inject = ['$locationProvider', '$translateProvider', 'logEnhancerProvider'];

  /**
   * @name config
   * @desc Enable HTML5 routing
   */
  function config($locationProvider, $translateProvider, logEnhancerProvider) {
      logEnhancerProvider.datetimePattern = 'HH:mm:ss';
      logEnhancerProvider.prefixPattern = '%s %s: ';
      $locationProvider.html5Mode(true);
      // this line replaces # to #! for SEO purposes
      $locationProvider.hashPrefix('!');
      //Basic translations
      $translateProvider.translations('en', {
          'ANALYTICS': 'Analytics',
          'ANDROID23BELOW':'Android 2.3 and blow',
          'ANDROID4TO44':'Android 4 to 4.4',
          'ANDROID5ABOVE':'Android 5 and above',
          'ANYCOMMENT':'Any Comment',
          'ANTIVIRUS_PLACEHOLDER':'i.e. Avg',
          'ABOUT_US_BODY': "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eu velit eu quam tempor fermentum.,'\
                Morbi auctor eget risus nec tempor. Fusce malesuada vitae elit in tincidunt.,'\
                Sed vitae felis vel sem fermentum accumsan. Nulla maximus malesuada massa vitae pulvinar.,'\
                Nulla orci nulla, convallis at arcu sit amet, lacinia elementum libero.,'\
                Nunc erat est, fringilla ac iaculis nec, sagittis malesuada metus. Aliquam eleifend nulla sem,,'\
                eget laoreet dolor egestas in. Curabitur aliquam lectus id nisi ultricies fermentum. Aliquam a nibh,'\
                facilisis dolor blandit varius. Ut vitae mattis massa. Vestibulum sit amet mauris elit. Nunc ullamcorper, ,'\
                magna ac consectetur luctus, quam neque interdum tortor, ut consectetur lectus augue in mauris.,'\
                Duis malesuada suscipit leo ut gravida. Aenean at porttitor lorem.,'\
                Mauris porta libero at nunc fermentum, eu feugiat tellus rhoncus.",
          'ABOUTUS':'About us',
          'ANTIVIRUSIFANY':'Antivirus if any',
          'ANDROID':'Android',
          'ACCOUNTDEACTIVATION':'Account Deactivation',
          'ACCOUNTDEACTIVATIONMSG':'Upon deactivation, all your information will be deleted from our server and you will not be able to login back with the same username and password. Note that reports that are submitted under your name remain in the system, they will only be marked as Anonymous. ',
          'BACK':'Back',
          'BELL': 'Bell',
          'BUSINESS': 'Business',
          'BANDWIDTH': 'Bandwidth',
          'CONTACT': 'Contact',
          'CHECK_ADDRESS_404':'Please make sure you have put the correct url in the address bar.',
          'COUNTRY':'Country',
          'CITY':'City',
          'COMMENTPLACEHOLDER':'Any additional comments or errors you want to let us know about',
          'CONFRMPASSWORD':'Confirm Password',
          'CREATEDAT':'Created At',
          'CUSTOMERSERVICE': 'Customer Service',
          'CONFIRMPASSWORD':'Confirm Password',
          'CURRENTPASSWORD':'Current Password',
          'CITY_PLACEHOLDER':'i.e. New York',
          'COUNTRY_PLACEHOLDER':'i.e. Switzerland',
          'DOWNLOAD_LINKS':'Download Links',
          'DEACTIVATE':'Deactivate',
          'DEACTIVATIONPASSWORD':'Please enter your password to deactivate the account',
          'ERROR_ALPHA_NUMERIC':'You can only use a-z, A-Z and 0-9 for this field',
          'ERROR_REQUIRED':'This field is required',
          'ERROR_PASSWORD_MATCH':'Passwords do not match.',
          'ERROR_PASSWORD_REGEX':'Password should contain at least one number, one small letter and one capital letter.',
          'ERROR_EMAIL':'Please enter a valid email address.',
          'ERROR_SHORT':'Too short! The minimum number of characters for this field is: ',
          'ERROR_LONG':'Too long! The maximum number of character for this fiels is:  ',
          'EMAIL':'Email',
          'ERROR_NUMBER':'Please enter a number',
          'ERORR_404':'Page does not exist',
          'EMAIL_DELIVERY':'Download via Email',
          'EMAIL_BODY':'You will automatically receive an email from us after sending this email.',
          'ENTER_EMAIL':'Please enter your email.',
          'FORGOTPASSWORD':'Forgot your password?',
          'FEEDBACK':'Feedback',
          'FAST':'Fast',
          'FAIL':'Fail',
          'FACEBOOKQUALITY':'Facebook Quality',
          'FIDO': 'Fido',
          'FIREWALLIFANY':'Firewall if any',
          'FIREWALL_PLACEHOLDER':'i.e. ZoneAlarm',
          'HOME':'Home',
          'IPHONE':'Iphone',
          'ISP':'Isp',
          'IOS':'IOS',
          'ISP_PLACEHOLDER':'i.e. AT&T',
          'INTERNAL_ERROR':'Internal server error, please reload the page',
          'LINUX':'Linux',
          'LOGIN': 'Login',
          'LOGOUT': 'Logout',
          'MAC':'Mac',
          'MAP_RESULTS': 'Map Results',
          'MESSAGE': 'Message',
          'MACOS':'Mac OS',
          'MODERATE':'Moderate',
          'NEXT':'Next',
          'NEWPASSWORD':'New Password',
          'NOMINAL_ISP_SPEED': 'Nominal ISP Speed',
          'NOTEXISTS': 'The page you are looking for does not exist.',
          'NOMINAL_DOWNLOAD_SPEED': 'Nominal Download Speed',
          'NOMINAL_UPLOAD_SPEED':'Nominal Upload Speed',
          'OVERALSATISFACTION':'Overall Satisfaction',
          'OPERATINGSYSTEM':'Operating System',
          'PASSWORD':'Password',
          'PROFILES': 'Profiles',
          'PROMOTION': 'Promotion',
          'PRICE_PLACEHOLDER':'30$',
          'PUBLIC': 'Public',
          'PRICE':'Price',
          'PROVINCE':'Province',
          'REGISTER': 'Register',
          'RETURN_HOME':'Go back to the homepage',
          'REPORTSUBMISSION': 'Submit a Report',
          'ROGERS': 'Rogers',
          'SET_YOUR_PASS' : 'Set your new password',
          'SUBMIT':'Submit',
          'SLOW':'Slow',
          'SERVICE_TYPE': 'Service Type',
          'SUBJECT': 'Subject',
          'SETTINGS':'Settings',
          'SUPER':'Super',
          'TERMS':'Terms and conditions of using this product',
          'TEST_YOUR_SPEED': 'Speed Test',
          'TITLE': 'ISPFY',
          'USERNAME':'Username',
          'USEREMAIL':'User Email',
          'UPDATEPASSWORD':'Update Password',
          'USERINFO':'User Info',
          'WIND': 'Wind',
          'WINDOWS':'Windows',
          'WINDOWSXPBELOW':'Windows XP and below',
          'WINDOWSVISTA':'Windows Vista',
          'WINDOWS7':'Windows 7',
          'WINDOWS8':'Windows 8',
          'WINDOWS10' : 'Windows 10',
          'YOUTUBEQUALITY':'Youtube Quality',
          '64k':'64 kbps',
          '128k':'128 kbps',
          '512k':'512 kbps',
          '1M':'1 Mbps',
          '2M':'2 Mbps',
          '3-5M':'3 to 5 Mbps',
          '6-9M':'6 to 9 Mbps',
          '10M':'10 Mbps and above',
          '':''
      });

      $translateProvider.preferredLanguage('en');
      $translateProvider.useCookieStorage();
      // Set the name of the cookie
      $translateProvider.storageKey('LANG');
      $translateProvider.useSanitizeValueStrategy(null)

  } //end of config
})();