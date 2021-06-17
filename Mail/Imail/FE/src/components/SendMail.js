import React, {useState} from 'react'

function SendMail() {
    const [formData, setFormData] = useState({});
    
    const handleChange = ({target}) => {
        const {name, value} = target;

        setFormData((prev) => ({
            ...prev, [name]: value
        }));
    }

    const handleSubmit = async(event) => {

        event.preventDefault();

        //lert(formData.userName);
        
        const response = await fetch('http://localhost:3001/email/createMail/?userName='
        +localStorage.getItem("userName")+"&content="+formData.content
        ,{method: 'POST',})
        .then(response => response.text())
        .then(idEmail => {
            if (idEmail != "-1" ){
                alert(idEmail);
                var recei =  formData.receiver.split(";");
                for (var i = 0; i < recei.length; i++) { 
                    const res = fetch('http://localhost:3001/email/addReceiver/?email_id='
                    +idEmail+"&receiver_name="+recei[i]
                    ,{method: 'POST',})
                    .then(res => res.text())
                    // eslint-disable-next-line no-loop-func
                    .then(contents => {
                        if (contents === "true"){
                            //Pass
                        }
                        else{
                            alert("Can't send to" + recei[i]);
                            //document.getElementById("signup-wrong").style.display = "block"
                        }
                    })
                    .catch(() => alert("Something went wrong"))
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
            <form onSubmit={handleSubmit}>
                <input type="text" name="receiver" placeholder="receiver name" onChange={handleChange}></input>
                <input type="text" name="content" placeholder="content" onChange={handleChange}></input>
                <input type="submit" value="Submit"></input>
            </form>
        </>     
    )
}

export default SendMail;