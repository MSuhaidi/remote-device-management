<script lang="ts">
    import { onMount } from "svelte";
    import { getDevices, runScript } from "../../lib/api";
    import { goto } from "$app/navigation";

    let devices = [];
    let scripts = ["health_check", "echo_test", "fail_test"];
    let selectedDeviceId: number;
    let selectedScript: string;

    onMount(async () => {
        try {
            devices = await getDevices();
            if (devices.length > 0) {
                selectedDeviceId = devices[0].id;
            }
            if (scripts.length > 0) {
                selectedScript = scripts[0];
            }
        } catch (error) {
            console.error(error);
        }
    });

    async function handleRunScript() {
        if (!selectedDeviceId || !selectedScript) {
            alert("Please select a device and a script.");
            return;
        }
        try {
            const execution = await runScript(selectedDeviceId, selectedScript);
            goto(`/executions/${execution.id}`);
        } catch (error) {
            console.error(error);
            alert("Failed to run script.");
        }
    }
</script>

<h1>Run Script</h1>

<div>
    <label for="device-select">Choose a device:</label>
    <select id="device-select" bind:value={selectedDeviceId}>
        {#each devices as device}
            <option value={device.id}>{device.name}</option>
        {/each}
    </select>
</div>

<div>
    <label for="script-select">Choose a script:</label>
    <select id="script-select" bind:value={selectedScript}>
        {#each scripts as script}
            <option value={script}>{script}</option>
        {/each}
    </select>
</div>

<button on:click={handleRunScript}>Run</button>
