import React, {useState} from 'react';

export default class SignUpServices {
    
    static signUp__ = async(userName, password, password2) => {
        return await fetch('http://localhost:3001/signUp/?userName='
                            +userName+"&password="+password+"&password2="+password2
                            ,{method: 'POST',})
    }
}
