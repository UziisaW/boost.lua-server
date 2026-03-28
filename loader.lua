-- boost.lua loader
-- Paste this into your executor. The token never touches this file.

local SERVER_URL = "https://YOUR-RAILWAY-APP.up.railway.app/script"
local SERVER_KEY = "YOUR_SERVER_KEY"   -- remove this line if you left SERVER_KEY blank in Railway

local ok, res = pcall(function()
    return (syn and syn.request or http and http.request or request)({
        Url     = SERVER_URL,
        Method  = "GET",
        Headers = {
            ["X-Key"] = SERVER_KEY,   -- remove this line if no SERVER_KEY
        },
    })
end)

if not ok or not res or res.StatusCode ~= 200 then
    warn("[boost.lua] Failed to fetch script: " .. tostring(res and res.StatusCode or res))
    return
end

loadstring(res.Body)()
