import React, {useState} from 'react';
import ListMail from './components/ListMail';

function UnreadPage() {
  return (
    <>
        <ListMail
            api = {"http://localhost:3001/mail/getUnreadMail/?userName=" + localStorage.getItem("userName")}
            boxChat = "none"
        />
        
    </>
  );
}

export default UnreadPage;  