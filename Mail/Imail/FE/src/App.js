import logo from './logo.svg';
import './App.css';
import SignUp from './components/SignUp'
import SignIn from './components/SignIn'
import Home from './components/Home';
import SendMail from './components/SendMail';
import HomePage from './components/Page/HomePage'
import SignOut from './components/SignOut';
import UnreadPage from './components/Page/UnreadPage';
import SentPage from './components/Page/SentPage';
import TrashPage from './components/Page/TrashPage';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';


function App() {
  return (
    <>
       <Router>
        <Switch>
          <Route path='/' exact component={HomePage} />
          <Route path='/SignUp' exact component={SignUp} />
          <Route path='/login' component={SignIn} />
          <Route path='/allMail' component={HomePage} />
          <Route path='/signOut' component={SignOut} />
          <Route path='/mail/unreadMail' component={UnreadPage} />
          <Route path='/mail/sentMail' component={SentPage} />
          <Route path='/mail/Trash' component={TrashPage} />
          <Route path='/mail/home' component={HomePage} />
        </Switch>
      </Router>
    </>
  );
}

export default App;
