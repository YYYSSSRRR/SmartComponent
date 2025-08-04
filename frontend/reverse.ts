import { createServer } from 'node:http';
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  LangGraphHttpAgent,
  copilotRuntimeNodeHttpEndpoint,
} from '@copilotkit/runtime';
 
const serviceAdapter = new ExperimentalEmptyAdapter();
 
const server = createServer((req, res) => {
const runtime = new (CopilotRuntime as any)({
    agents: {
        'sample_agent': new LangGraphHttpAgent({url: "http://localhost:8000/copilokit"}),
    }
});
 
  const handler = copilotRuntimeNodeHttpEndpoint({
    endpoint: '/copilotkit',
    runtime,
    serviceAdapter,
  });
 
  return handler(req, res);
});
 
server.listen(4000, () => {
  console.log('Listening at http://localhost:4000/copilotkit');
});