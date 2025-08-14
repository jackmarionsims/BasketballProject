import { useState } from 'react'
import "@mantine/core/styles.css";
import "@mantine/dates/styles.css";
import "@mantine/charts/styles.css";
import './App.css'

import { MantineProvider, Container, Title } from "@mantine/core";
import  TeamSchedule  from "./TeamSchedule";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { type FilterParams } from './api';
import GameDetailsPage from './GameDetailsPage';
import  FilteredGames  from './FilteredGames';
import { Group, Button, Box, Text } from '@mantine/core';

export default function App() {
  const homeFilter: FilterParams = {
    pts_min: 120,
    pts_max: 120,
  };

  const visitorFilter: FilterParams = {
    pts_min: 130,
    pts_max: 130,
  };

  return (
    <MantineProvider>
      <Router>
        <Group w="100%">
          {/* <Title order={1}>NBA Stats Dashboard</Title> */}
          <Routes>
            {/* <Route path="/" element={<TeamSchedule teamName="Atlanta Hawks" season={2024} />} /> */}
            <Route path="/" element={<FilteredGames />} />
            <Route path="/game/:gameId" element={<GameDetailsPage />} />
          </Routes>
        </Group>
      </Router>
    </MantineProvider>
  );
}