import React from "react";
import { Heading, Flex } from "@chakra-ui/react";

const Header = () => {
  return (
      <Flex
          as="nav"
          align="center"
          justify="space-between"
          wrap="wrap"
          padding="0.5rem"
          bg="gray.400"
      >
        <Flex align="center">
          <Heading as="h1" size="lg" padding={5} >Resume Improver</Heading>
        </Flex>
      </Flex>
  );
};

export default Header;
