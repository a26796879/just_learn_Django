local celery_shutdown_url = "'http://backend.myvnc.com:5555/api/worker/shutdown/";
local Authorization = "'Authorization: Basic dXNlcjE6cGFzc3dvcmQx'";
local push_docker(repo) = {
    kind:"pipeline",
    name:"publish-services_"+repo,
    steps:[{
      name: "deploy-services",
      image: "plugins/docker",
      settings: {
        username: { "from_secret": "docker_username" },
        password: { "from_secret": "docker_password" },
        cache_from: "a26796879/"+ repo,
        repo: "a26796879/" + repo,
        auto_tag: true
        },
      },
    ],    
};

local publish_services = {
    kind:"pipeline",
    name:"publish_services",
    steps:[{
      name: "deploy-services",
      image: "appleboy/drone-ssh",
      settings: {
        username: "user",
        host: { "from_secret": "service_host" },
        key: { "from_secret": "id_rsa" },
        script: [
            "ls",
            "cd just_learn_Django",
            "docker-compose stop",
            "sudo git reset --hard",
            "sudo git pull",
            "sudo docker-compose build",
            "docker pull a26796879/just_learn_django",
            "docker pull a26796879/just_learn_celery",
            "docker-compose up -d",
        ],
      },
    },
  ],
};

local publish_workers(host,celery_name,Authorization) = {
    kind:"pipeline",
    name:"publish_to_workers_"+ host,
    steps:[{
      name: "deploy-workers_"+ host,
      image: "appleboy/drone-ssh",
      settings: {
        host: { "from_secret": host },
        key: { "from_secret": "id_rsa" },
        username: "user",
        script: [
            "ls",
            "cd just_learn_Django",
            "sudo git reset --hard",
            "sudo git pull",
            "curl --location --request POST "+celery_shutdown_url +celery_name+ " --header "+Authorization,
            "python3 -m celery -A news.tasks worker -l INFO --detach"
        ],
      }
    },
  ],
};


[
    push_docker("just_learn_django"),
    push_docker("just_learn_celery"),
    publish_services,
    publish_workers("celery1_host","celery@odoo'",Authorization),
    publish_workers("celery2_host","celery@rabbitmq-server'",Authorization),
    publish_workers("celery3_host","celery@celery'",Authorization)
]