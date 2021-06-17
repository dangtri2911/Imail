import React, {useState} from 'react';
import ListMail from '../components/ListMail';

function TrashPage() {
  return (
    <>
        <ListMail
            api = {"http://localhost:3001/mail/getDeletedMail/?userName=" + localStorage.getItem("userName")}
            boxChat = "none"
            restore = "true"
        />
        
    </>
  );
}

export default TrashPage;