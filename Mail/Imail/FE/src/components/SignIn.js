import React, {useState} from 'react';
import '../css/login.css';
import SignInServices from '../services/signin_service';

function SignIn(props) {
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
        
        const response = SignInServices.signIn__(formData.userName,formData.passWord)
        .then(response => response.text(), localStorage.setItem("userName", formData.userName) /*document.cookie = "userName = formData.userName";*/)
        .then(contents => {
            if (contents === "true"){
                window.location.replace("http://localhost:3000/");
            }
            else{
                try {
                    document.getElementById("signin-wrong").innerHTML = "Invalid username or password";
                    document.getElementById("signin-wrong").style.display = "block";
                    document.getElementById("signOut-info").style.display = "none";
                } catch (error) {}
        
                
            }
        })
        .catch(() => {
            try {
                document.getElementById("signin-wrong").innerHTML = "Invalid username or password";
                document.getElementById("signin-wrong").style.display = "block";
                document.getElementById("signOut-info").style.display = "none";
            } catch (error) {}
            
        })
    }

    return(
        <>
            <div class="body_">
                <img src={process.env.PUBLIC_URL + '/images/bg_6.jfif'} class="col-md-6 col-12 bg_left_lg" alt="view.jpg"></img>
                <form class="col-md-6 col-12 login_form_contain" onSubmit={handleSubmit}>
                    <div class="login_form">
                        <h3>Login</h3>
                        <div className="alert alert-danger" id="signin-wrong" style={{display: "None"}}>Invalid</div>
                        {props.signOut&&<div className="alert alert-info" id="signOut-info">{props.signOut}</div>}
                        <div>
                            <label>User Name: </label>
                            <input type="text" name="userName" id="username" placeholder="userName" onChange={handleChange}></input>
                        </div>
                        <div>
                            <label>Password: </label>
                            <input type="passWord" name="passWord" id="password1" placeholder="password" onChange={handleChange}></input>
                        </div>
                        <div class="remember">
                            <label><input type="checkbox" name="remember"></input> Remember me</label>
                        </div>
                        <div class="submit_btn">
                            <input type="submit" value="Submit" class="submit"></input>
                        </div>
                        <div class="account_remain">
                            <p>Don't have an account? <a href="/sign-up"> Sign up</a></p>
                        </div>
                        <div>
                            <h5> Login with social Media</h5>
                            <div class="social_media_contain">
                                <i class="fab fa-facebook-square"></i>
                                <i class="fab fa-instagram"></i>
                                <i class="fab fa-google"></i>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </>     
    )
}

export default SignIn;