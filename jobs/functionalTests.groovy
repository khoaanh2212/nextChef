job("nextchef-functional-tests") {
  label("docker")
  steps {
    shell("""
rm -fr *
rm -fr .git
rm -fr .gitignore
""")
    copyArtifacts("nextchef-build-app") {
      includePatterns("*/**")
      fingerprintArtifacts(false)
      buildSelector {
        upstreamBuild()
      }
    }
    shell("""
commit_hash=int_\$(git rev-parse HEAD)
cd backend_project
make functional-tests TAG=\$commit_hash REGISTRY=docker.apiumtech.io
""")
  }
  authorization {
    permissionAll("jenkins-admin")
  }
  publishers {
    configure {
      it / 'publishers' / 'au.com.centrumsystems.hudson.plugin.buildpipeline.trigger.BuildPipelineTrigger'(plugin: 'build-pipeline-plugin@1.4.7') {
        configs('')
        downstreamProjectNames("nextchef-deploy-staging")
      }
    }
    mailer("thuy.le@apiumtech.com, jose.barroso@apiumtech.com, binh.tran@apiumtech.com, rafa.hidalgo@apiumtech.com, lam.pham@apiumtech.com, rost.tok@apiumtech.com, oscar.galindo@apiumtech.com, sergi.fernandez@apiumtech.com", true, true)
  }
}
