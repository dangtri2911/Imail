import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import '../css/box_chat.css';

function BoxChat(props) {

    const [formData, setFormData] = useState({});

    const [display, setDisplay] = useState(props.boxChat);

    const handleChange = ({target}) => {
        const {name, value} = target;

        setFormData((prev) => ({
            ...prev, [name]: value
        }));
    }

    const handleSubmit = async(event) => {
        event.preventDefault();
        //alert(formData.userName);
        const response = await fetch('http://localhost:3001/signIn/?userName='
        +formData.userName+"&password="+formData.passWord
        ,{method: 'POST',})
        .then(response => response.text(), localStorage.setItem("userName", formData.userName) /*document.cookie = "userName = formData.userName";*/)
        .then(contents => {
            if (contents === "true"){
                window.location.replace("http://localhost:3000/");
            }
            else{
                alert("Error");
            }
        })
        .catch(() => {
            alert("Something wrong");
        })
    }

    const close_box_chat = async() => {
      alert('123');
      document.getElementById('box_chat__').style.display ="block";
    }

  return (
    <>
        <form class="box_chat" id="box_chat__" onsubmit={handleSubmit} style={{display: display}}>
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
  );
}

export default BoxChat;