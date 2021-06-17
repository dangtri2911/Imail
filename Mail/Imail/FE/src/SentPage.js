import React, {useState} from 'react';
import ListMail from './components/ListMail';

function SentPage() {
  return (
    <>
        <ListMail
            api = {"http://localhost:3001/mail/getSentMail/?userName=" + localStorage.getItem("userName")}
            boxChat = "none"
        />
        
    </>
  );
}

export default SentPage;