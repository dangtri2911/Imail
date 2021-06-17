import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import ListMail from '../ListMail';
import BoxChat from '../BoxChat'

function HomePage() {

  return (
    <>
        <ListMail
            api = {"http://localhost:3001/mail/getReceiveMail/?userName=" + localStorage.getItem("userName")}
            boxChat = "none"
        />
        
    </>
  );
}

export default HomePage;