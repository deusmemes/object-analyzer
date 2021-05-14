import React from "react";
import {Dropdown, Icon, Nav, Navbar} from "rsuite";

const Menu = ({}) => {
    return (
        <Navbar>
            <Navbar.Body>
                <Nav>
                    <Nav.Item icon={<Icon icon="home"/>}>Home</Nav.Item>
                    <Nav.Item>News</Nav.Item>
                    <Nav.Item>Products</Nav.Item>
                    <Dropdown title="About">
                        <Dropdown.Item>Company</Dropdown.Item>
                        <Dropdown.Item>Team</Dropdown.Item>
                        <Dropdown.Item>Contact</Dropdown.Item>
                    </Dropdown>
                </Nav>
                <Nav pullRight>
                    <Nav.Item icon={<Icon icon="cog"/>}>Settings</Nav.Item>
                </Nav>
            </Navbar.Body>
        </Navbar>
    )
}

export default Menu;