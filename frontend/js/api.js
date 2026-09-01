/**
 * API Client Module for HV Myra Matchday Board
 * Centralized REST endpoint interactions with FastAPI backend.
 */

export async function fetchTeamConfig(teamId = 'MO10') {
    const res = await fetch(`/api/config?team_id=${encodeURIComponent(teamId)}`);
    if (!res.ok) throw new Error(`Failed to fetch config for team ${teamId}`);
    return await res.json();
}

export async function fetchActiveTactics(teamId = 'MO10', matchDate = '', opponent = '', quarter = 'Q1') {
    const params = new URLSearchParams({
        team_id: teamId,
        match_date: matchDate,
        opponent: opponent,
        quarter: quarter
    });
    const res = await fetch(`/api/tactics/active?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch tactics snapshot');
    return await res.json();
}

export async function saveTactics(payload, token = '') {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const res = await fetch('/api/tactics', {
        method: 'POST',
        headers,
        body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to save tactics');
    return await res.json();
}

export async function fetchTeams() {
    const res = await fetch('/api/teams');
    if (!res.ok) throw new Error('Failed to fetch teams listing');
    return await res.json();
}

export async function createTeam(teamData) {
    const res = await fetch('/api/teams', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(teamData)
    });
    if (!res.ok) throw new Error('Failed to create team');
    return await res.json();
}
