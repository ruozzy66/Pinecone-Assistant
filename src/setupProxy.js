const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'https://api.pinecone.io',
      changeOrigin: true,
      pathRewrite: {
        '^/api': '/v1/assistant',
      },
    })
  );
};