import { Grid, Text, RangeSlider, Group, NumberInput, Table } from "@mantine/core";
import { Link } from "react-router-dom";
import { formatDate } from "./FilteredGames";

export default function GamesTable({ games }: { games: any[] }) {
    return (<Table striped highlightOnHover withTableBorder style={{ width: "100%" }}>
                <Table.Thead>
                    <Table.Tr>
                        <Table.Th style={{ textAlign: 'center' }}>Date</Table.Th>
                        <Table.Th style={{ textAlign: 'center' }}>Visitor Team</Table.Th>
                        <Table.Th style={{ textAlign: 'center' }}>Home Team</Table.Th>
                        <Table.Th style={{ textAlign: 'center' }}></Table.Th>
                    </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                {games.map((game) => (
                    <Table.Tr key={game["Game ID"]}>
                        <Table.Td>{formatDate(game["Date"])}</Table.Td>
                        <Table.Td>
                            {game["Visitor Team"]}
                        </Table.Td>
                        <Table.Td>{game["Home Team"]}</Table.Td>
                        <Table.Td>
                            <Link to={`/game/${game["Game ID"]}`} target="_blank" rel="noopener noreferrer">
                                Box Score
                            </Link>
                        </Table.Td>
                    </Table.Tr>
                ))}
                </Table.Tbody>
            </Table>) }