/**
 * Front-End Library for working with CyberSource service
 * @author Ivan Melnik
 * @version 1.0
 * @constructor
 * @returns CyberSource {Object} instance
 */
app.define('vendor/cybersource', [
    'jquery',
    'app.resources',
    'component/form/Form'
], function (jQuery, app, Form) {
    var CyberSource = new (function(){
    	
        var configuration, radioPayment, applyButton, submitButton, paymentForm, ccOwnerField, ccNumberField, ccSubmitBtn, loader, cvnField, errors;
        
        /**
         * Sets configurations
         * @public
         * @param config : Object
         */
        this.setConfiguration = function(config){
            if(!config || !(config instanceof Object)) return false;
            configuration = config;
            return this;
        }
        
        /**
         * main initialization, for all payment methods. Should be invoked in pt_payment.isml
         * @public
         */
        this.init = function(){
            
            radioPayment = jQuery('input[name="' + configuration.selectors.methodsSwitcherRadio + '"]');
            applyButton = jQuery('button[name="' + configuration.selectors.applyBtn + '"]');
            submitButton = jQuery("#" + configuration.selectors.paymentForm).find('button[type=submit]');
            cvnField = jQuery('[name^="' + configuration.selectors.cvnField + '"]');
            //convert json-safe representation of the reg-exp to real RegExp object
            configuration.creditCardNumberRegexp = new RegExp(decodeURIComponent(configuration.creditCardNumberRegexp));
            this.initGiftCards();
            this.scrollDownCvn();
        }
        
        /**
         * scrolling down to CVN field, if it exist
         * @public
         */
        this.scrollDownCvn = function(){
            if(jQuery(".top-error-messages").length == 0 && cvnField.length > 0){
                var offset = jQuery(".checkoutpayment").offset();
                if(offset !== null && offset !== undefined){
                    window.scrollTo(offset.left, offset.top);
                    var errorMess = cvnField.closest(".formfield").find("span.errormessage");
                    if(errorMess.length > 0 && jQuery.trim(errorMess.text()) != ''){
                        errorMess.show();
                    }else{
                        if (!configuration.singleStep) { // TODO check on Brazil
                            cvnField.focus(); 
                        }
                    }
                }
            }
        }
        
        /**
         * Initialization Credit Card form
         * @public
         */
        this.initCreditCard = function($componentEl){
        	$componentEl = $componentEl || jQuery(document);
        	
            paymentForm = $componentEl.find("#" + configuration.selectors.paymentForm);
            ccOwnerField = jQuery("[name='" + configuration.selectors.ccOwnerField + "']");
            ccNumberField = jQuery("[data-static-name='" + configuration.selectors.ccNumberField + "']");
            ccSubmitBtn = jQuery("[name='" + configuration.selectors.ccSubmitBtn + "']");
            loader = jQuery("<div class='" + configuration.loaderClass + "'>").insertAfter(ccSubmitBtn).hide();
            
            var signCreditCardFieldsSubmitted = false;
            var busy = false;
            
            /**
             * Init triggering of selected installments plan for updating totals
             */
            var installments = jQuery("[name='" + configuration.selectors.ccInstallments + "']");
            installments.on('change', function(e) {
                var selectedText = jQuery(e.currentTarget).find('option:selected').text();
                jQuery(app).trigger('installmentsPlanSelected', [selectedText]);
            });  
            
            var formError = paymentForm.parent().find('.errorform');
            if(formError.length == 0){
                formError = jQuery('<div class="errorform" />').insertBefore(paymentForm);
            } else {
                formError = formError.not('#giftcarderror');
            }
            formError.hide();
            
            /**
             * Show loader spin
             * @private
             */
            function showLoader(){
                loader.show();
            }
            
            /**
             * Hide loader spin
             * @private
             */
            function hideLoader(){
                loader.hide();
            }
            
            /**
             * Displaying errors
             * @private
             * @param error : Object    Could be a string, boolean
             */
            function errorHandler(error){
                if(!error || typeof(error) != "string"){
                    error = app.resources["SERVER_ERROR"];
                }
                formError.html('<span>' + error + '</span>').show();
                ccSubmitBtn.removeClass('disabled').attr("disabled", false);
                hideLoader();
            }
            
            /**
             * Submitting form to CyberSource Security Acceptance SOP (Silent Order Post)
             * @private
             * @param data  :   Object      jqHXR response data
             */
            function submitSOP(data){

                paymentForm.find('input,select').attr("disabled","disabled");
                ccSubmitBtn.removeClass('disabled').attr("disabled", false);
                
                for (var fieldName in data.fieldsToSubmit) {
                    if(fieldName in data.fieldsToSubmit && data.fieldsToSubmit[fieldName]){
                        paymentForm.append(jQuery('<input type="hidden" name="' + fieldName + '"/>').val(data.fieldsToSubmit[fieldName]));
                    }
                }
                if(configuration.singleStep) {
                    paymentForm.append(jQuery('<input type="hidden" name="card_cvn"/>').val(cvnField.val()));
                }
                paymentForm.append(jQuery('<input type="hidden" name="card_number"/>').val(ccNumberField.val().replace(/\D/g,'')));
                
                busy = false;
                signCreditCardFieldsSubmitted = true;
                
                paymentForm.submit();
            }

            var isIE9OrBelow = function()
            {
               return /MSIE\s/.test(navigator.userAgent) && parseFloat(navigator.appVersion.split("MSIE")[1]) < 10;
            }
            
            /**
             * Preparing and requesting signing CreditCard fields (request to DW server side)
             * @private
             */
            function submitSigningFields(){
                if(signCreditCardFieldsSubmitted || busy) return false;
                var validState = Form.getById( configuration.selectors.paymentForm ).getValidState(true);
                
                // do signing fields
                var formFields = paymentForm.serializeArray();
                
                //In IE9 select elements are missing from formFields
                if( isIE9OrBelow() ) {
	                var missingFields = {};
	                var selects = paymentForm.find('select:not(:disabled)').each(function(){
	                	missingFields[this.name] = {
	                		name : this.name,
	                		value : jQuery(this).val() || ""
	                	};
	                });
	                for( var field in formFields ){
	                	if(formFields.hasOwnProperty(field) && missingFields.hasOwnProperty(formFields[field].name) ) {
	                		delete missingFields[formFields[field].name];
	                	}
	                }
	                for( var field in missingFields ){
	                	if( missingFields.hasOwnProperty(field) ) {
	                		formFields.push(missingFields[field]);
	                	}
	                }
                }
                
                if ( validState === false ) {
                    submitButton.removeClass('disabled');
                    return false;
                }
                if(configuration.singleStep) {
                    cvnField.attr("disabled", "disabled");
                }
                
                ccNumberField.attr("disabled", "disabled");
                ccSubmitBtn.attr("disabled", "disabled");
                
                var request = jQuery.ajax({
                    type: "POST",
                    url: configuration.signDataURL,
                    data: formFields,
                    dataType: "json",
                    beforeSend: function(jqXHR, settings){
                        formError.html('').hide();
                        signCreditCardFieldsSubmitted = false;
                        
                        if(notFilledFields(formFields)){
                            ccSubmitBtn.removeClass('disabled').attr("disabled", false);
                            ccNumberField.attr("disabled", false);
                            if(configuration.singleStep) {
                                cvnField.attr("disabled", false);
                            }
                            return false;
                        }
                        
                        showLoader();
                        busy = true;
                    },
                    success: function(data, textStatus, jqXHR){
                    	var errorMessage;
                    	if ('hasErrors' in data){
                            if(data.hasErrors === false && (typeof(data.fieldsToSubmit) == 'object')) {
                                ccNumberField.attr("disabled", false);
                                if(configuration.singleStep) { 
                                    cvnField.attr("disabled", false);
                                }
                                submitSOP(data);
                                return true;
                            }else if(data.hasErrors === true && typeof(data.redirectUrl) != 'undefined'){
                                window.location.href = data.redirectUrl;
                                return false;
                            }
                            errorMessage = data.hasErrors;
                    	} else if ('success' in data && !data.success){
                    		errorMessage = data.error;
                    		jQuery('.layer-prevent-dblclick').remove();
                    		jQuery('.processing').removeClass('processing btn-processing').hide();
                    		jQuery('#giftcards').prepend("<div class='errorform' id='giftcarderror'><span>"+errorMessage+"</span></div>");
                    	}
                    	
                		errorHandler(errorMessage)
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        if(jqXHR.status == '200' && textStatus == 'parsererror'){
                            window.location.href = configuration.signDataURL;
                            return false;
                        }
                        ccNumberField.attr("disabled", false);
                        errorHandler();
                    },
                    complete: function(jqXHR, textStatus){
                        busy = false;
                    }
                });
            }
            
            /**
             * Checking for non filled fields of CreditCard form
             * @private
             * @param formFields    : Array     Array of Objects with attributes "name", "value". CreditCard form fields.
             */
            function showMissingError(field){
            	if(field.length == 0 || jQuery.trim(field.val()) == ''){
	                errors = true;
	                //triggers FormField event from component/form/Form
	                field.trigger('onMissingField');
            	}        
            }
            
            function notFilledFields(formFields){
                errors = false;
                
                for(var i = 0; i < formFields.length; i++){
                    var field = jQuery('[name="' + formFields[i].name + '"]');
                    showMissingError(field);
                }
                
                return errors;
            }
            
            /**
             * Handling Submit form event
             * @private
             */
            paymentForm.on('submit', function(e){
                if(busy) return false;
                if(!signCreditCardFieldsSubmitted){
                    submitSigningFields();
                    return false;
                }
                return true;
            });
            
            return this;
        }
        
        this.initGiftCards = function ( configurationData ) {
            var config = configurationData || configuration;
            var newGiftcardBlock = jQuery('.newgiftcard');
            var addNewGiftcardBtn = jQuery('#showNewGiftcard');
            var newGiftCardNumber = jQuery('#' + config.selectors.gcNewGiftCardNumber);
            var newGiftCardPin = jQuery('#' + config.selectors.gcNewGiftCardPin);
            var applyNewGiftCard = jQuery('#' + config.selectors.gcApplyGiftCard);
            var checkboxUsegiftcards = jQuery('#' + config.selectors.gcUseGiftCard);
            var paymentForm = jQuery('#' + config.selectors.paymentForm + ',.' + config.selectors.paymentForm+',.recurring-payment-form');
            var giftcards = jQuery('#giftcards');
            var paymentsSwitcher = jQuery('.co-paymentmethods');
            var deliveryActions = jQuery('.co-delivery-actions,.co-actions');
            
            changeVisibility( checkboxUsegiftcards.prop('checked') );
            
            function changeVisibility( isSvsEnabled ) {
                if( isSvsEnabled ) {
                    // show SVS giftcards
                    giftcards.removeClass("unvisible"); 
                    // hide payments if Order is fully covered by giftgcards
                    if( paymentForm.hasClass('canHideMainPayment') ) {
                        paymentForm.addClass('unvisible');
                        paymentsSwitcher.addClass('unvisible');
                        deliveryActions.addClass('unvisible');
                    }
                    // add parameter to the form that giftcards are included
                    jQuery('<input>').attr({
                        type: 'hidden',
                        id: 'usesvsgiftcard',
                        'class' : 'usesvsgiftcard-input',
                        name: 'usesvsgiftcard',
                        value: isSvsEnabled
                    }).appendTo(paymentForm);
                } else {
                    // hide SVS giftcards
                    giftcards.addClass("unvisible");
                    // show payments
                    paymentForm.removeClass('unvisible');
                    paymentsSwitcher.removeClass('unvisible');
                    deliveryActions.removeClass('unvisible');
                    // remove form parameter indicating that giftcards are included
                    paymentForm.find('.usesvsgiftcard-input').remove(); 
                    
                }
                
                if ( jQuery('#giftcarderror').length ) {
                    newGiftcardBlock.show();
                    addNewGiftcardBtn.hide();
                    paymentForm.find('.errorform').show();
                }
            }
            
            checkboxUsegiftcards.on('change', function() {
                changeVisibility( checkboxUsegiftcards.prop('checked') );
            });
            
            function toggleApplyButton () {
                if( newGiftCardNumber.val() && newGiftCardPin.val() ) {
                    applyNewGiftCard.prop('disabled', false).removeClass('disabled');
                } else {
                    applyNewGiftCard.prop('disabled', true).addClass('disabled');
                }
            }
            
            newGiftCardNumber.on('keydown keyup change paste', toggleApplyButton );
            newGiftCardPin.on('keydown keyup change paste', toggleApplyButton );
            
            addNewGiftcardBtn.on('click', function() {
                newGiftcardBlock.show();
                addNewGiftcardBtn.hide();
            });
            
        };
    })();
    
    return CyberSource;
});