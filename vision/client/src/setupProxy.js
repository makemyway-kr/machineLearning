import { createProxyMiddleware } from "http-proxy-middleware";

module.exports = (app) => {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://localhost:5555",
      changeOrigin: true,
    })
  );
  app.use(
    "/ws-stomp",
    createProxyMiddleware({ target: "http://localhost:8080", ws: true })
  );
};