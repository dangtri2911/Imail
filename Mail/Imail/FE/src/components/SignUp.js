import React,{useState} from 'react';
import User_Form from './User_Form';

function SignUp() {
    const [formData, setFormData] = useState({});
    
    const handleChange = ({target}) => {
        const {name, value} = target;

        setFormData((prev) => ({
            ...prev, [name]: value
        }));
    }

    const handleSubmit = async(event) => {
        event.preventDefault();
        //alert(formData.passWord + "-" + formData.passWord2);
        if (formData.passWord != formData.passWord2){
            document.getElementById("signin-wrong").innerHTML = "Your passwords not match";
            document.getElementById("signin-wrong").style.display = "block";
        }else{
            document.getElementById("signin-wrong").style.display = "none";
            const response = await fetch('http://localhost:3001/signUp/?userName='
            +formData.userName+"&password="+formData.passWord+"&password2="+formData.passWord2
            ,{method: 'POST',})
            .then(response => response.text() 
            /*document.cookie = "userName = formData.userName";*/)
            .then(contents => {
                if (contents === "true"){
                    window.location.replace("http://localhost:3000/");
                }   
                else{
                    document.getElementById("signin-wrong").innerHTML = "Username has existed";
                    document.getElementById("signin-wrong").style.display = "block";
                }
            })
            .catch(() => {
                document.getElementById("signin-wrong").innerHTML = "Something wrong !!!";
                document.getElementById("signin-wrong").style.display = "block";
            })
        }

        //alert(formData.userName);
        
        
    }

    return(
        <>
            <div class="body_" style={{backgroundImage   : "url('/images/bg_12.jpg')"}}>
                <form class="col-12 login_form_contain" onSubmit={handleSubmit}>
                    <div class="login_form">
                        <h3>Sign Up</h3>
                        <div className="alert alert-danger" id="signin-wrong" style={{display: "None"}}>Invalid</div>
                        <div> <label>User Name: </label>
                            <input type="text" name="userName" id="userName" placeholder="UserName" onChange={handleChange}></input>
                        </div>
                        <div>
                            <label>Password: </label>
                            <input type="password" name="passWord" id="passWord" placeholder="Password" onChange={handleChange}></input>
                        </div>
                        <div>
                            <label>Confirm Password: </label>
                            <input type="password" name="passWord2" id="passWord2" placeholder="Confirm password" onChange={handleChange}></input>
                        </div>
                        <br/>
                        <div class="submit_btn">
                            <input type="submit" value="Submit" class="submit" name=""></input>
                        </div>
                    </div>
                </form>
            </div>
        </>     
    )
}

export default SignUp;