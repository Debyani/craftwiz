select complete_url from url where
lower(complete_url ) like ? order by depth asc ;