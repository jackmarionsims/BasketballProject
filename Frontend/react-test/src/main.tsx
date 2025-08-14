import React from "react";
import ReactDOM from "react-dom/client";
import { MantineProvider } from "@mantine/core";
import App from "./App";

import "@mantine/core/styles.css"; // must be imported before MantineProvider

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <MantineProvider
      theme={{
        fontFamily: "Inter, sans-serif",
        defaultRadius: "md",
      }}
    >
      <App />
    </MantineProvider>
  </React.StrictMode>
);

