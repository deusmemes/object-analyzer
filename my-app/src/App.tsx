import React from 'react';
import logo from './logo.svg';
import './App.css';

import {Button, Container, Content, Footer, Header, Panel, PanelGroup} from 'rsuite';

// import default style
import 'rsuite/dist/styles/rsuite-default.css';
import Menu from "./components/Menu/Menu";
import UploadImage from "./components/UploadImage/UploadImage";
import SelectModel from "./components/SelectModel/SelectModel"; // or 'rsuite/dist/styles/rsuite-default.css'

function App() {
    return (
        <Container>
            <Header><Menu/></Header>
            <Content style={{width: '60%', marginLeft: '20%'}}>
                <Container style={{ marginTop: '3em' }}>
                    <SelectModel models={[
                        {name: 'Снимки', id: 1, description: 'd'},
                        {name: 'Поля', id: 2, description: 'd'},
                    ]}/>
                </Container>
                <Container style={{ marginTop: '3em' }}>
                    <UploadImage/>
                </Container>
            </Content>
            <Footer></Footer>
        </Container>
    )
}

export default App;
