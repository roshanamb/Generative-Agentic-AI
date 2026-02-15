from pydantic import BaseModel, Field, field_validator, model_validator

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=50)

    @field_validator('name')
    def validate_name(cls, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError('Name must be between 3 and 50 characters long')
        return value
        
        # if not value.isalpha():
        #     raise ValueError('Name must contain only alphabetic characters')
        # return value

class SignUpData(BaseModel):
    email: str = Field(..., regex=r'^\S+@\S+\.\S+$')
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @field_validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value
    
    @field_validator('confirm_password')
    def validate_confirm_password(cls, value, values):
        if 'password' in values and value != values['password']:
            raise ValueError('Passwords do not match')
        return value
    
    @model_validator(mode='after') ## This validator runs after all fields validation & field validators have been executed
    def validate_passwords_match(cls, values):
        if values.password != values.confirm_password:
            raise ValueError('Passwords do not match')
        return values