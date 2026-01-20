<script lang="ts">
    import { onMount } from "svelte";
    import { getDevices } from "../../lib/api";

    let devices = [];

    onMount(async () => {
        try {
            devices = await getDevices();
        } catch (error) {
            console.error(error);
        }
    });
</script>

<h1>Devices</h1>

<table>
    <thead>
        <tr>
            <th>Device ID</th>
            <th>Name</th>
            <th>Status</th>
            <th>Last Seen</th>
        </tr>
    </thead>
    <tbody>
        {#each devices as device}
            <tr>
                <td>{device.id}</td>
                <td>{device.name}</td>
                <td>{device.status}</td>
                <td>
                {new Date(device.last_seen + 'Z').toLocaleString(undefined, {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: true
                })}
            </td>
            </tr>
        {/each}
    </tbody>
</table>

<style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
    }
</style>
