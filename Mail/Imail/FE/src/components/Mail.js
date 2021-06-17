import React from 'react';
import { useState, useEffect  } from 'react';
import { Link } from 'react-router-dom';
import MailServices from '../services/mail_Service';

function Mail(props) {
    // alert(props.deleted_date);
    const [display, setDisplay] = useState("none");

    const handleRead = async(event) => {
      MailServices.readMail(localStorage.getItem('userName'),props.id)
      .then(response => response.text())
      .then(setDisplay("block"))
    }
    const handleDelete = async(event) => {
        event.preventDefault();

        //lert(formData.userName);
        
        const response = MailServices.deleteMail(localStorage.getItem('userName'),props.id)
        .then(response => response.text())
        .then(contents => {
            if (contents === "true"){
                alert('Delete success');
                window.location.reload();
            }
            else{
              alert('Something went wrong');
            }
        })
        .catch(() => {
            alert('Something went wrong');
        })
    }

    const handleRestore = async(event) => {
        event.preventDefault();

        //lert(formData.userName);
        
        const response = MailServices.restoreMail(localStorage.getItem('userName'),props.id)
        .then(response => response.text())
        .then(contents => {
            if (contents === "true"){
                alert('Restore success');
                window.location.reload();
            }
            else{
              alert('Something went wrong');
            }
        })
        .catch(() => {
            alert('Something went wrong');
        })
    }

    return (
      <>
          <div class='col email'>
            <div class="col col-3 sender"> {props.userName}</div>
            <div class="col col-7 content"> {props.content} </div>
            <div class="col col-2 action_"> 
                <a onClick={handleRead} class="far fa-eye"></a>
                {props.restore&&
                     <a onClick={handleRestore} class="far fas fa-trash-restore"></a>
                }
                {/* <a href={'/mail/DeleteMail/?userName=' + localStorage.getItem('userName') + "&mail_del=" + props.id} class="far fa-trash-alt"></a> */}
               
                {!props.restore&&
                  <a class="far fa-trash-alt" onClick={handleDelete}></a>
                }
            </div>
          </div>
          <div class="view_mail_contain" style={{display: display}}>
            <form class="view_mail">
                <div class="col title">
                    <span>Mail</span>
                    <i onClick={() => setDisplay("none")} class="fas fa-times"></i>
                </div>
                <div class="box_input__">
                    <input type="text" disabled name="receiver" placeholder="To ..." value={'From: ' + props.userName}></input>
                </div>
                <div class="box_content">
                    <textarea disabled name="content" value={props.content}></textarea>
                </div>
                {props.restore&&
                  <span>{'Deleted Date: ' + props.deleted_date}</span>
                }
                {!props.restore&&
                  <span>{'Created Date: ' + props.created_date}</span>
                }
            </form>
          </div>
      </>
    );
}

export default Mail;