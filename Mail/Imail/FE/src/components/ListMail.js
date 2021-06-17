import React from 'react';
import Mail from './Mail';
import { useState, useEffect  } from 'react';
import '../css/email.css';
import '../css/home.css';
import '../css/navbar.css';
import '../css/box_chat.css';
import SendMailServices from '../services/sendMail_service';
import ListMailServices from '../services/list_mail_service';

function ListMail(props){

    if(!localStorage.getItem("userName")){
        window.location = "http://localhost:3000/login"
    }

    const [data, setData] = useState("");
    // const [box, setBox] = useState("none");
    const [display, setDisplay] = useState(props.boxChat);
    const [formData, setFormData] = useState({});
    const [alert_danger, setAlert_danger] = useState(null);
    const [alert_info, setAlert_info] = useState(null);
    const [updateTime, updateEmail] = useState(0);
    
    useEffect(() => {
        ListMailServices.getListMail(props.api)
          .then(response => response.json())
          .then(contents => setData(contents));

          // Update per 2m
          const timer = setInterval(() => {
            updateEmail(updateTime + 1);
            //alert('rerender');
          }, 120000);

          clearInterval(timer);
          
    }, [updateTime]);

    
    //setInterval(updateEmail(updateTime + 1), 120000);

    const handleChange = ({target}) => {
        const {name, value} = target;

        setFormData((prev) => ({
            ...prev, [name]: value
        }));
    }

    const handleLogOut = () => {
        localStorage.removeItem("userName");
        window.location.href = 'localhost:3000/login';
    }
    // const handleSubmit = SendMailServices.sendMail;
    const handleSubmit = async(event) => {

        event.preventDefault();

        setAlert_danger(null);
        setAlert_info(null);
        
        const response = SendMailServices.sendMail(formData.content)
        .then(response => response.text())
        .then(idEmail => {
            alert("id "+idEmail);
            if (idEmail != "-1" ){
                //alert(idEmail);
                var recei =  formData.receiver.split(" ");
                for (var i = 0; i < recei.length; i++) { 
                    const res = SendMailServices.addReceiver(idEmail,recei[i])
                    .then(res => res.text())
                    // eslint-disable-next-line no-loop-func
                    .then(contents => {
                        if (contents === "true"){
                            setAlert_info("Sent successfully");
                            updateEmail(updateTime+1);
                        }
                        else{
                            setAlert_danger("Undefined receiver");
                        }
                    })
                    // eslint-disable-next-line no-loop-func
                    .catch(() => { setAlert_info("Something went wrong")})
                }
            }
            else{
                alert('Error');
                //document.getElementById("signup-wrong").style.display = "block"
            }
        })
        .catch(() => alert("Something went wrong"))
    }

    return(
        <>
            <div id="index_contain" style={{backgroundImage: 'linear-gradient(rgba(0, 0, 0, 0.5),rgba(0, 0, 0, 0.3)),url(/images/a5.jpg)'}}>
                <header id="header">
                        <a class="sign_out__" href="#" onClick={handleLogOut}>
                            Sign out
                        </a>
                        <a class="user__" href="#">
                            {localStorage.getItem("userName")}
                        </a>
                </header>
                <div class="my_container">
                    <div>
                        <div class="col col-3">
                            <button class="btn_contain" onClick={() => setDisplay('block')}>
                                <label>Send Mail</label>
                                <i class="fas fa-plus-circle add_btn"></i>
                            </button>
                            <ul class="navBar_">    
                                <li><a href="/mail/home"><i class="fas fa-home"></i> Home </a></li>
                                <li><a href="/mail/unread-mail"> <i class="fas fa-envelope"></i> Unread </a></li>
                                <li><a href="/mail/sent-mail"> <i class="fas fa-share-square"></i> Sent </a></li>
                                <li><a href="/mail/trash"> <i class="fas fa-trash"></i> Trash </a></li>
                                <li><a href="/user-info"> <i class="fas fa-user"></i> UserInfo </a></li>
                            </ul>
                        </div>
                        <div class="col col-9">
                            { alert_info !== null &&
                                <div class="alert alert-info text-center">{alert_info}</div>
                            }
                            {   alert_danger !== null &&
                                <div class="alert alert-danger text-center"> {alert_danger}</div>
                            }
                            
                            {data ? 
                                data.map(row => {
                                    return (
                                                 <Mail 
                                                    key= {row.id}
                                                    userName = {row.userName}
                                                    content = {row.content}
                                                    id = {row.id}
                                                    restore = {props.restore}
                                                    created_date = {row.created_date}
                                                    deleted_date = {row.deleted_date}
                                                 />
                                    )
                                })
                            :<div/>
                            }
                            
                        </div>
                    </div>
                </div>
            </div>
            
            <form class="box_chat" id="box_chat__" onSubmit={handleSubmit} style={{display: display}}>
                <div class="col title">
                    <span>Thư mới</span>
                    <i onClick={() => setDisplay('none')} class="fas fa-times"></i>
                </div>
                <div class="box_input__">
                    <input type="text" name="receiver" onChange={handleChange} placeholder="To ..."></input>
                </div>
                <div class="box_content">
                    <textarea name="content" onChange={handleChange}></textarea>
                </div>
                <input type="submit" value="Submit"  class="box_submit"></input>
            </form>
        </>
    )
}

export default ListMail;