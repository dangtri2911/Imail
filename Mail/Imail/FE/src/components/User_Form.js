import React, {useState} from 'react'

function User_Form() {
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
        
        const response = await fetch('http://localhost:3001/signUp/?userName='
        +formData.userName+"&password="+formData.passWord
        ,{method: 'POST',})
        .then(response => response.text())
        .then(contents => {
            if (contents === "true"){
                alert("Signup successfully");
                //window.location.replace("http://localhost:3000/signin/");
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
                <input type="text" name="userName" placeholder="userName" onChange={handleChange}></input>
                <input type="passWord" name="passWord" placeholder="password" onChange={handleChange}></input>
                <input type="submit" value="Submit"></input>
            </form>
        </>     
    )
}

export default User_Form;