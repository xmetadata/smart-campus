<template>
  <div class='app-container'>
    <el-input placeholder='搜索' v-model='filterText' style='margin-bottom:30px'></el-input>

    <el-tree
      :data="treedata"
      node-key="id"
      :expand-on-click-node="false"
      :filter-node-method="filterNode"
      :render-content="renderContent"
      ref="tree2">
    </el-tree>
  </div>
</template>

<script>
let id = 1000

export default {
  data() {
    const data = [
      {
        id: 1,
        label: '陕西省',
        children: [
          {
            id: 30,
            label: '咸阳'
          },
          {
            id: 4,
            label: '西安市',
            children: [
              {
                id: 9,
                label: '雁塔区',
                children: [
                  {
                    id: 20,
                    label: '高新一小',
                    children: [
                      {
                        id: 20,
                        label: '1年级',
                        children: [
                          {
                            id: 20,
                            label: '2班',
                            children: [
                              {
                                id: 20,
                                label: '小明'
                              },
                              {
                                id: 30,
                                label: '小李'
                              }
                            ]
                          },
                          {
                            id: 30,
                            label: '3班'
                          }
                        ]
                      },
                      {
                        id: 30,
                        label: '2年级'
                      }
                    ]
                  },
                  {
                    id: 30,
                    label: '逸翠园中学',
                    children: [
                      {
                        id: 20,
                        label: '1年级',
                        children: [
                          {
                            id: 20,
                            label: '2班',
                            children: [
                              {
                                id: 20,
                                label: '小明'
                              },
                              {
                                id: 30,
                                label: '小李'
                              }
                            ]
                          },
                          {
                            id: 30,
                            label: '3班'
                          }
                        ]
                      },
                      {
                        id: 30,
                        label: '2年级'
                      }
                    ]
                  }
                ]
              },
              {
                id: 10,
                label: '未央区'
              }
            ]
          }
        ]
      },
      {
        id: 2,
        label: '山西',
        children: [
          {
            id: 5,
            label: '太原'
          },
          {
            id: 6,
            label: '包头'
          }
        ]
      }
    ]
    return {
      treedata: JSON.parse(JSON.stringify(data)),
      filterText: ''
    }
  },

  watch: {
    filterText(val) {
      this.$refs.tree2.filter(val)
    }
  },

  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },

    append(data) {
      this.$prompt('请输入标题', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /\S/,
        inputErrorMessage: '格式不正确'
      }).then(({ value }) => {
        const newChild = { id: id++, label: value, children: [] }
        if (!data.children) {
          this.$set(data, 'children', [])
        }
        data.children.push(newChild)
        this.$message({
          type: 'success',
          message: '添加成功'
        })
      })
    },

    remove(node, data) {
      this.$confirm('此操作将永久删除, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const parent = node.parent
        const children = parent.data.children || parent.data
        const index = children.findIndex(d => d.id === data.id)
        children.splice(index, 1)
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      })
    },

    renderContent(h, { node, data, store }) {
      return (
        <span style='flex: 1; display: flex; align-items: center; justify-content: space-between; font-size: 14px; padding-right: 8px;'>
          <span>
            <span>{node.label}</span>
          </span>
          <span>
            <el-button-group>
              <el-button style='font-size: 12px;' type='text' icon='el-icon-edit' on-click={ () => this.append(data) }>编辑&nbsp;&nbsp;</el-button>
              <el-button style='font-size: 12px;' type='text' icon='el-icon-circle-plus-outline' on-click={ () => this.append(data) }>添加&nbsp;&nbsp;</el-button>
              <el-button style='font-size: 12px;' type='text' icon='el-icon-remove-outline' on-click={ () => this.remove(node, data) }>删除</el-button>
            </el-button-group>
          </span>
        </span>)
    }
  }
}
</script>
