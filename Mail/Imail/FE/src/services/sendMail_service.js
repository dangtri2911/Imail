import React, {useState} from 'react';
import ListMail from '../components/ListMail';

export default class SendMailServices {
    
    static sendMail = async(content) => {
        return await fetch('http://localhost:3001/email/createMail/?userName='
        +localStorage.getItem("userName")+"&content=" + content
        ,{method: 'POST',})
        // return response;
    }

    static addReceiver = async(idEmail,receiver_name) => {
        return await fetch('http://localhost:3001/email/addReceiver/?email_id='
        +idEmail+"&receiver_name="+ receiver_name
        ,{method: 'POST',})
        // return response;
    }
}
