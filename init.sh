export $(cat .env | xargs) && rails c

# Create dirs for localstorages
mkdir ./"$LS_BASE_TEMP_DIR"/
mkdir -p "$LS_BASE_TEMP_DIR"/n1/"$LS_WORK_DIR"
mkdir -p "$LS_BASE_TEMP_DIR"/n2/"$LS_WORK_DIR"
mkdir -p "$LS_BASE_TEMP_DIR"/n3/"$LS_WORK_DIR"
mkdir -p "$LS_BASE_TEMP_DIR"/n4/"$LS_WORK_DIR"
mkdir -p "$LS_BASE_TEMP_DIR"/n5/"$LS_WORK_DIR"
mkdir -p "$LS_BASE_TEMP_DIR"/n6/"$LS_WORK_DIR"
mkdir -p "$LS_BASE_TEMP_DIR"/n7/"$LS_WORK_DIR"
mkdir -p "$LS_BASE_TEMP_DIR"/n8/"$LS_WORK_DIR"
mkdir -p "$LS_BASE_TEMP_DIR"/n9/"$LS_WORK_DIR"
mkdir -p "$LS_BASE_TEMP_DIR"/n10/"$LS_WORK_DIR"


# Create dirs for logs
mkdir ./"$SPP_LOG_TEMP_PATH"/
mkdir -p ./"$SPP_LOG_TEMP_PATH"/n1
mkdir -p ./"$SPP_LOG_TEMP_PATH"/n2
mkdir -p ./"$SPP_LOG_TEMP_PATH"/n3
mkdir -p ./"$SPP_LOG_TEMP_PATH"/n4
mkdir -p ./"$SPP_LOG_TEMP_PATH"/n5
mkdir -p ./"$SPP_LOG_TEMP_PATH"/n6
mkdir -p ./"$SPP_LOG_TEMP_PATH"/n7
mkdir -p ./"$SPP_LOG_TEMP_PATH"/n8
mkdir -p ./"$SPP_LOG_TEMP_PATH"/n9
mkdir -p ./"$SPP_LOG_TEMP_PATH"/n10

# Create dirs for plugins archive
mkdir ./"$PL_BASE_TEMP_DIR"/
mkdir -p ./"$PL_BASE_TEMP_DIR"/n1
mkdir -p ./"$PL_BASE_TEMP_DIR"/n2
mkdir -p ./"$PL_BASE_TEMP_DIR"/n3
mkdir -p ./"$PL_BASE_TEMP_DIR"/n4
mkdir -p ./"$PL_BASE_TEMP_DIR"/n5
mkdir -p ./"$PL_BASE_TEMP_DIR"/n6
mkdir -p ./"$PL_BASE_TEMP_DIR"/n7
mkdir -p ./"$PL_BASE_TEMP_DIR"/n8
mkdir -p ./"$PL_BASE_TEMP_DIR"/n9
mkdir -p ./"$PL_BASE_TEMP_DIR"/n10