import React, { useState, useEffect } from "react";
import { Table, Loader, Alert } from "@mantine/core";
import { getGame, getTeam } from "./api";
import { Link } from 'react-router-dom';

export default function TeamSchedule({ teamName, season }: { teamName: string; season: number }) {
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
    <div>
      <h2>{teamName} Schedule</h2>
      <ul>
        {games.map((game) => (
          <li key={game["Game ID"]}>
            {/* Clickable link/button */}
            <Link to={`/game/${game["Game ID"]}`}>
                Date: {game["Date"]} —{" "}
                {teamName === game["Home Team"] ? <strong>{game["Home Team"]}</strong> : game["Home Team"]}{" "}
                @{" "}
                {teamName === game["Visitor Team"] ? <strong>{game["Visitor Team"]}</strong> : game["Visitor Team"]}
                - {game["Date"]}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
