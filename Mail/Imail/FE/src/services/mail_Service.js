import React, {useState} from 'react';
export default class MailServices {
    
    static readMail = async(userName, mail_id) => {
        return await fetch('http://localhost:3001/mail/readMail/?userName='+userName+'&mail_read='+mail_id)
    }

    static deleteMail = async(userName, mail_id) => {
        return await fetch('http://localhost:3001/mail/DeleteMail/?userName='+userName+'&mail_del='+mail_id
        ,{method: 'POST',})
    }
    
    static restoreMail = async(userName, mail_id) => {
        return await fetch('http://localhost:3001/mail/RestoreMail/?userName='+userName+'&mail_del='+mail_id
        ,{method: 'POST',})
    }
}
