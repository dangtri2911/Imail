import logo from './logo.svg';
import './App.css';
import SignUp from './components/SignUp';
import SignIn from './components/SignIn';
import HomePage from './HomePage';
import UnreadPage from './UnreadPage';
import SentPage from './SentPage';
import TrashPage from './TrashPage';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';


function App() {
  return (
    <>
       <Router>
        <Switch>
          <Route path='/' exact component={HomePage} />
          <Route path='/sign-up' exact component={SignUp} />
          <Route path='/login' component={SignIn} />
          <Route path='/all-mail' component={HomePage} />
          <Route path='/mail/unread-mail' component={UnreadPage} />
          <Route path='/mail/sent-mail' component={SentPage} />
          <Route path='/mail/trash' component={TrashPage} />
          <Route path='/mail/home' component={HomePage} />
        </Switch>
      </Router>
    </>
  );
}

export default App;
