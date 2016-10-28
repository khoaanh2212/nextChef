job("nextchef-build-app") {
  label("docker")
  logRotator {
    numToKeep(3)
  }
  scm {
    git {
      remote {
        url("https://github.com/Cookbooth/backend.git")
        branch("master")
        credentials("b254c1e8-5a27-42b0-b97c-8996ecaf8371")
      }
      clean()
    }
  }

  triggers {
    scm("H/3 * * * *")
  }

  steps {
    shell("""
commit_hash=int_\$(git rev-parse HEAD)
cd backend_project
make build-app TAG=\$commit_hash REGISTRY=docker.apiumtech.io
""")
  }

  authorization {
    permissionAll("jenkins-admin")
  }

  publishers {
    archiveArtifacts {
      pattern('**/*')
      onlyIfSuccessful()
      defaultExcludes(false)
    }

    downstream("nextchef-functional-tests")
    mailer("thuy.le@apiumtech.com, jose.barroso@apiumtech.com, binh.tran@apiumtech.com, rafa.hidalgo@apiumtech.com, lam.pham@apiumtech.com, rost.tok@apiumtech.com, oscar.galindo@apiumtech.com, sergi.fernandez@apiumtech.com", true, true)
  }
}
