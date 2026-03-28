-- hi, im 6raveyard and ur looking at the loader.lua!

local SERVER_URL = "https://web-production-66781.up.railway.app"
local SERVER_KEY = "boost.luaishotbro"

local ok, res = pcall(function()
    return (syn and syn.request or http and http.request or request)({
        Url     = SERVER_URL,
        Method  = "GET",
        Headers = {
            ["X-Key"] = SERVER_KEY,
        },
    })
end)

if not ok or not res or res.StatusCode ~= 200 then
    warn("[boost.lua] Failed to fetch script: " .. tostring(res and res.StatusCode or res))
    return
end

loadstring(res.Body)()
