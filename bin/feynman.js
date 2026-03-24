#!/usr/bin/env node
const v = process.versions.node.split(".").map(Number);
if (v[0] < 20) {
  console.error(`feynman requires Node.js 20 or later (you have ${process.versions.node})`);
  console.error("upgrade: https://nodejs.org or nvm install 20");
  process.exit(1);
}
import("../dist/index.js");
