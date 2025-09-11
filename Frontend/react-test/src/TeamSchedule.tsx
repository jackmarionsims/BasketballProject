import React, { useState, useEffect, use } from "react";
import { Table, Loader, Alert, Container } from "@mantine/core";
import { getGame, getTeam } from "./api";
import { Link } from 'react-router-dom';
import GamesTable from "./GamesTable";
import { useParams, useSearchParams } from "react-router-dom";

const teamAbbreviations: Record<string, string> = { 
    "ATL": "Atlanta Hawks",
    "BRK": "Brooklyn Nets",
    "BKN": "Brooklyn Nets",
    "BOS": "Boston Celtics",
    "CHA": "Charlotte Bobcats",
    "CHH": "Charlotte Hornets",
    "CHO": "Charlotte Hornets",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DAL": "Dallas Mavericks",
    "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons",
    "GSW": "Golden State Warriors",
    "HOU": "Houston Rockets",
    "IND": "Indiana Pacers",
    "LAC": "Los Angeles Clippers",
    "LAL": "Los Angeles Lakers",
    "MEM": "Memphis Grizzlies",
    "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks",
    "MIN": "Minnesota Timberwolves",
    "NJN": "New Jersey Nets",
    "NOH": "New Orleans Hornets",
    "NOP": "New Orleans Pelicans",
    "NOK": "Oklahoma City Hornets",
    "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder",
    "ORL": "Orlando Magic",
    "PHI": "Philadelphia 76ers",
    "PHX": "Phoenix Suns",
    "PHO": "Phoenix Suns",
    "POR": "Portland Trail Blazers",
    "SEA": "Seattle SuperSonics",
    "SAC": "Sacramento Kings",
    "SAS": "San Antonio Spurs",
    "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz",
    "VAN": "Vancouver Grizzlies",
    "WAS": "Washington Wizards",
    "WSB": "Washington Bullets"
}

const DEFAULT_SEASON = 2025;

export default function TeamSchedule() {
  const teamAbbrev = useParams().teamName;
  if (!teamAbbrev) throw new Error("teamName param is required");
  const teamName = teamAbbreviations[teamAbbrev.toUpperCase()] || teamAbbrev;
  const [searchParams] = useSearchParams();
  const season = Number(searchParams.get("season")) || DEFAULT_SEASON;
  const [games, setGames] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    getTeam(teamName, season)
      .then((res) => {
        console.log(res[0])
        setGames(res);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [teamName, season]);

  if (loading) return <Loader />;
  if (error) return <Alert color="red">{error}</Alert>;

  return (
    <Container size='sm' mt="lg">
      <h2>{teamName} Schedule</h2>
      <GamesTable games={games} />
    </Container>
  );
}
