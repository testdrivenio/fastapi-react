import React from "react";
import { Heading, Flex, Separator } from "@chakra-ui/react";

const Header = () => {
  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="1rem"
      bg="gray.400"
      width="100%"
      zIndex="1000"
    >
      <Flex align="center" as="nav" mr={5}>
        <Heading as="h1" size="sm">Todos</Heading>
        <Separator />
      </Flex>
    </Flex>
  );
};

export default Header;