import React, { Component } from 'react';
import { Text } from 'react-native';

import { Button, Card, CardSection, Input, Spinner } from './common';

import axios from 'axios';

class LoginForm extends Component {
    state = { email: '', password: '', error: '', loading: false };

    onLoginSuccess () {
        this.setState({
            email: '',
            password: '',
            loading: false,
            error: '',
        })
    }
    onLoginFail (data) {
        console.log(data);
        if (data.email){
            response_error = data.email;
        } else if (data.password) {
            response_error = data.password;
        }
        this.setState({
            password: '',
            loading: false,
            error: response_error,
        })
    }

    renderButton () {
        if (this.state.loading) {
            return <Spinner size="small" />;
        }
        return (
            <Button onPress={this.onButtonPress.bind(this)}>
                Log In
            </Button>
        );
    }

    onButtonPress() {
        this.setState({error: '', loading: true })
        axios.post('http://localhost:5000/login_standard/', {
            'email': this.state.email,
            'password': this.state.password,
        })
        .then(this.onLoginSuccess.bind(this))
        .catch((error) => {this.onLoginFail(error.response.data)})
    }

    render() {
        return (
            <Card>
                <CardSection>
                    <Input
                        placeholder='user@email.com'
                        label='E-mail'
                        value={this.state.email}
                        onChangeText={email => this.setState({ email })} 
                    />
                </CardSection>
                <CardSection>
                    <Input
                        label='Password'
                        placeholder='password'
                        secureTextEntry={true}
                        value={this.state.password}
                        onChangeText={password => this.setState({ password })} 
                    />
                </CardSection>
                <Text style={styles.errorTextStyle}>{this.state.error}</Text>
                <CardSection>
                    {this.renderButton()}
                </CardSection>
            </Card>
        )
    }
}

const styles = {
    errorTextStyle: {
        fontSize: 20,
        alignSelf: 'center',
        color: 'red',
    }
};

export default LoginForm;