import React, {useState} from 'react';

export default class SignInServices {
    
    static signIn__ = async(userName, password) => {
        return await fetch('http://localhost:3001/signIn/?userName='
                            +userName+"&password="+password
                            ,{method: 'POST',})
    }
}
