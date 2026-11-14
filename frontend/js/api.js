export async function fetchUserAuthMe(token = '', teamId = 'MO10') {
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(`/api/auth/me?team_id=${encodeURIComponent(teamId)}`, { headers });
    if (!res.ok) throw new Error('Failed to fetch user authentication info');
    return await res.json();
}

export async function fetchTeamConfig(teamId = 'MO10', token = '') {
    const headers = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    const res = await fetch(`/api/config?team_id=${encodeURIComponent(teamId)}`, { headers });
    if (!res.ok) throw new Error(`Failed to fetch config for team ${teamId}`);
    return await res.json();
}

export async function saveTeamConfig(teamId, configPayload, token = '') {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const res = await fetch(`/api/config?team_id=${encodeURIComponent(teamId)}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(configPayload)
    });
    if (!res.ok) throw new Error('Failed to save team config');
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

export async function createTeam(teamData, token = '') {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const res = await fetch('/api/teams', {
        method: 'POST',
        headers,
        body: JSON.stringify(teamData)
    });
    if (!res.ok) throw new Error('Failed to create team');
    return await res.json();
}

