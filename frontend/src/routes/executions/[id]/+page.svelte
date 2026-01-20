<script lang="ts">
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { getExecution } from "../../../lib/api";

    let execution = null;
    let interval;

    async function fetchExecution() {
        try {
            const executionId = parseInt($page.params.id);
            execution = await getExecution(executionId);
            if (execution.status !== 'pending' && execution.status !== 'running') {
                clearInterval(interval);
            }
        } catch (error) {
            console.error(error);
            clearInterval(interval);
        }
    }

    onMount(() => {
        fetchExecution();
        interval = setInterval(fetchExecution, 3000);
        return () => clearInterval(interval);
    });
</script>

<h1>Execution Details</h1>

{#if execution}
    <div>
        <strong>Script Name:</strong> {execution.script_name}
    </div>
    <div>
        <strong>Status:</strong> {execution.status}
    </div>
    <div>
        <strong>Stdout:</strong>
        <pre>{execution.stdout}</pre>
    </div>
    <div>
        <strong>Stderr:</strong>
        <pre>{execution.stderr}</pre>
    </div>
    <div>
        <strong>Started At:</strong> {new Date(execution.started_at).toLocaleString()}
    </div>
    <div>
        <strong>Finished At:</strong> {execution.finished_at ? new Date(execution.finished_at).toLocaleString() : 'N/A'}
    </div>
{:else}
    <p>Loading execution details...</p>
{/if}

<style>
    pre {
        background-color: #f4f4f4;
        padding: 10px;
        border: 1px solid #ddd;
    }
</style>
