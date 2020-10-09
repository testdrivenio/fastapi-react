import React from "react";
import {Heading, Flex, Divider} from "@chakra-ui/core";

const Header = props => {
    return (
        <Flex
            as="nav"
            align="center"
            justify="space-between"
            wrap="wrap"
            padding="0.5rem"
            bg="gray.400"
            // color="white"
            {...props}
        >
            <Flex align="center" mr={5}>
                <Heading as="h1" size="sm">
                    Todos
                </Heading>
                <Divider />
            </Flex>
        </Flex>
    );
};

export default Header;