class Login:
    
    def __init__(self, email, password):
         self.email = email
         self.password = password

    
    def login(self,email,password): 
        if(valid_email(self,email)):
            if(valid_password(self,email,password)):
               return("response: succesful login")
            else:
                return("response:password not valid")
        else:
            return("response:email not valid")
         


    def valid_email(self, email):
        '''
        check email is in database

        if(response):
            return true
        else:
            return false 

        '''
        pass

    def valid_password(self,email,password):
        '''
        check password is in database

        if(response):
            return true
        else:
            return false 

        '''
        pass

    def forgot_password(self,email,new_password):
        '''
        if(valid_email):
            send email to reset password 
        '''
        pass

    
    