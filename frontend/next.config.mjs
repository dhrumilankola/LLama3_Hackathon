/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    // Add a rule to handle the dlv package
    config.module.rules.push({
      test: /[\\/]node_modules[\\/]dlv[\\/]/,
      use: {
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env'],
          plugins: ['@babel/plugin-transform-modules-commonjs']
        }
      }
    });

    return config;
  },
}

export default nextConfig;