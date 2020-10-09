import React from "react";
import {render} from 'react-dom';
import {ThemeProvider} from "@chakra-ui/core";
import Header from "./Components/Header";
import Todos from "./Components/Todos";

function App({ children }) {
    return (
        <ThemeProvider>
            <Header />
            <Todos />
            {children}
        </ThemeProvider>
    )
}

const rootElement = document.getElementById("root");
render(<App />, rootElement)
